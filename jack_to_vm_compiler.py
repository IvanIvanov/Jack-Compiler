#!/usr/bin/python
#
# Copyright (c) 2011 Ivan Vladimirov Ivanov (ivan.vladimirov.ivanov@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


__author__ = "Ivan Vladimirov Ivanov (ivan.vladimirov.ivanov@gmail.com)"


import os

import symbol_table


class CodeGenerationError(Exception):
  def __init__(self, message):
    self.message = message


class JackToVMCompiler(object):

  def __init__(self):
    self.if_count = 0
    self.while_count = 0
    self.class_name = ""

  def CompileVMCode(self, jack_program):
    env = symbol_table.SymbolTable(None)
    return os.linesep.join(self.CompileClass(jack_program, env))

  def CompilePushCommand(self, segment, index):
    return ["push %s %d" % (segment, index)]

  def CompilePopCommand(self, segment, index):
    return ["pop %s %d" % (segment, index)]

  def CompileArithmeticCommand(self, command):
    return [command]

  def CompileLabelCommand(self, label):
    return ["label %s" % (label)]

  def CompileGotoCommand(self, label):
    return ["goto %s" % (label)]

  def CompileIfCommand(self, label):
    return ["if-goto %s" % (label)]

  def CompileCallCommand(self, name, n_args):
    return ["call %s %d" % (name, n_args)]

  def CompileFunctionCommand(self, name, n_locals):
    return ["function %s %d" % (name, n_locals)]

  def CompileReturnCommand(self):
    return ["return"]

  def CompileClass(self, jack_class, env):
    result = []
    self.class_name = jack_class.class_name
    for class_var_dec in jack_class.class_var_decs:
      result.extend(self.CompileClassVarDec(class_var_dec, env))
    for subroutine_dec in jack_class.subroutine_decs:
      result.extend(self.CompileSubroutineDec(subroutine_dec, env))
    return result

  def CompileClassVarDec(self, var_dec, env):
    for var_name in var_dec.var_names:
      name = var_name.identifier
      var_type = self._GetVarType(var_dec.var_type.var_type)
      env.Insert(var_name.identifier, var_type, var_dec.scope.keyword)
    return []

  def CompileSubroutineDec(self, subroutine, env):
    new_env = symbol_table.SymbolTable(env)
    sub_type = subroutine.subroutine_type.keyword
    return getattr(self, "Compile" + sub_type.capitalize() + "Dec")(
        subroutine, new_env)

  def CompileFunctionDec(self, subroutine, env):
    for param in subroutine.param_list:
      var_type = self._GetVarType(param[0].var_type)
      var_name = param[1].identifier
      env.Insert(var_name, var_type, "argument")

    result = []
    result.extend(self.CompileFunctionCommand(
        "%s.%s" % (self.class_name.identifier, subroutine.name.identifier),
        self._CountLocalVariables(subroutine)))
    result.extend(self.CompileSubroutineBody(subroutine.body, env))
    return result

  def CompileMethodDec(self, subroutine, env):
    env.Insert("this", self.class_name.identifier, "argument")
    for param in subroutine.param_list:
      var_type = self._GetVarType(param[0].var_type)
      var_name = param[1].identifier
      env.Insert(var_name, var_type, "argument")

    result = []
    result.extend(self.CompileFunctionCommand(
        "%s.%s" % (self.class_name.identifier, subroutine.name.identifier),
         self._CountLocalVariables(subroutine)))
    result.extend(self.CompilePushCommand("argument", 0))
    result.extend(self.CompilePopCommand("pointer", 0))
    result.extend(self.CompileSubroutineBody(subroutine.body, env))
    return result

  def CompileConstructorDec(self, subroutine, env):
    for param in subroutine.param_list:
      var_type = self._GetVarType(param[0].var_type)
      var_name = param[1].identifier
      env.Insert(var_name, var_type, "argument")

    result = []
    result.extend(self.CompileFunctionCommand(
        "%s.%s" % (self.class_name.identifier, subroutine.name.identifier),
        1 + self._CountLocalVariables(subroutine)))
    result.extend(self.CompilePushCommand("constant", env.CountKind("field")))
    result.extend(self.CompileCallCommand("Memory.alloc", 1))
    result.extend(self.CompilePopCommand("pointer", 0))
    result.extend(self.CompileSubroutineBody(subroutine.body, env))
    return result

  def CompileSubroutineBody(self, body, env):
    result = []
    for var_dec in body.var_decs:
      result.extend(self.CompileVarDec(var_dec, env))
    result.extend(self.CompileStatements(body.statements, env))
    return result

  def CompileVarDec(self, var_dec, env):
    for var_name in var_dec.var_names:
      var_type = self._GetVarType(var_dec.var_type.var_type)
      var_name = var_name.identifier
      env.Insert(var_name, var_type, "local")
    return []

  def CompileStatements(self, statements, env):
    result = []
    for statement in statements.statements:
      result.extend(self.CompileStatement(statement, env))
    return result

  def CompileStatement(self, statement, env):
    name = statement.statement.__class__.__name__
    return getattr(self, "Compile" + name)(
        statement.statement, env)

  def CompileLetStatement(self, statement, env):
    name = statement.let_statement.__class__.__name__
    return getattr(self, "Compile" + name)(
        statement.let_statement, env)

  def CompileRegularLetStatement(self, statement, env):
    value = env.Lookup(statement.var_name.identifier)
    if value is None:
      raise CodeGenerationError("Unknown identifier %s" % (
          statement.var_name.identifier))

    if value[1] == "field":
      value = (value[0], "this", value[2])
 
    result = []
    result.extend(self.CompileExpression(statement.expression, env))
    result.extend(self.CompilePopCommand(value[1], value[2]))
    return result

  def CompileArrayLetStatement(self, statement, env):
    value = env.Lookup(statement.var_name.identifier)
    if value is None:
      raise CodeGenerationError("Unknown identifier %s" % (
          statement.var_name.identifier))

    if value[1] == "field":
      value = (value[0], "this", value[2])

    result = []
    result.extend(self.CompileExpression(statement.expression, env))
    result.extend(self.CompileExpression(statement.index_expression, env))
    result.extend(self.CompilePushCommand(value[1], value[2]))
    result.extend(self.CompileArithmeticCommand("add"))
    result.extend(self.CompilePopCommand("pointer", 1))
    result.extend(self.CompilePopCommand("that", 0))
    return result

  def CompileIfStatement(self, statement, env):
    name = statement.if_statement.__class__.__name__
    return getattr(self, "Compile" + name)(
        statement.if_statement, env)

  def CompileRegularIfStatement(self, statement, env):
    self.if_count += 1
    label = "end-if-%d" % (self.if_count)

    result = []
    result.extend(self.CompileExpression(statement.expression, env))
    result.extend(self.CompileArithmeticCommand("not"))
    result.extend(self.CompileIfCommand(label))
    result.extend(self.CompileStatements(statement.statements, env))
    result.extend(self.CompileLabelCommand(label))
    return result

  def CompileIfElseStatement(self, statement, env):
    self.if_count += 1
    label1 = "else-clause-%d" % (self.if_count)
    label2 = "end-if-%d" % (self.if_count)

    result = []
    result.extend(self.CompileExpression(statement.expression, env))
    result.extend(self.CompileArithmeticCommand("not"))
    result.extend(self.CompileIfCommand(label1))
    result.extend(self.CompileStatements(statement.if_statements, env))
    result.extend(self.CompileGotoCommand(label2))
    result.extend(self.CompileLabelCommand(label1))
    result.extend(self.CompileStatements(statement.else_statements, env))
    result.extend(self.CompileLabelCommand(label2))
    return result

  def CompileWhileStatement(self, statement, env):
    self.while_count += 1
    label1 = "start-while-%d" % (self.while_count)
    label2 = "end-while-%d" % (self.while_count)

    result = []
    result.extend(self.CompileLabelCommand(label1))
    result.extend(self.CompileExpression(statement.expression, env))
    result.extend(self.CompileArithmeticCommand("not"))
    result.extend(self.CompileIfCommand(label2))
    result.extend(self.CompileStatements(statement.statements, env))
    result.extend(self.CompileGotoCommand(label1))
    result.extend(self.CompileLabelCommand(label2))
    return result

  def CompileDoStatement(self, statement, env):
    result = []
    result.extend(self.CompileSubroutineCall(statement.subroutine_call, env))
    result.extend(self.CompilePopCommand("temp", 0))
    return result

  def CompileReturnStatement(self, statement, env):
    name = statement.return_statement.__class__.__name__
    return getattr(self, "Compile" + name)(
        statement.return_statement, env)

  def CompileExpressionReturnStatement(self, statement, env):
    result = []
    result.extend(self.CompileExpression(statement.expression, env))
    result.extend(self.CompileReturnCommand())
    return result

  def CompileNoExpressionReturnStatement(self, statement, env):
    result = []
    result.extend(self.CompilePushCommand("constant", 0))
    result.extend(self.CompileReturnCommand())
    return result

  def CompileExpression(self, expression, env):
    result = []
    result.extend(self.CompileTerm(expression.first_term, env))
    for op, term in expression.op_term_list:
      result.extend(self.CompileTerm(term, env))
      result.extend(self.CompileOperator(op, env))
    return result

  def CompileTerm(self, term, env):
    name = term.term.__class__.__name__
    if name == "tuple":
      return self.CompileArrayAccess(term.term, env)
    else:
      return getattr(self, "Compile" + name)(term.term, env)

  def CompileOperator(self, op, env):
    operator_table = {
        "+": self.CompileArithmeticCommand("add"),
        "-": self.CompileArithmeticCommand("sub"),
        "&": self.CompileArithmeticCommand("and"),
        "|": self.CompileArithmeticCommand("or"),
        "<": self.CompileArithmeticCommand("lt"),
        ">": self.CompileArithmeticCommand("gt"),
        "=": self.CompileArithmeticCommand("eq"),
        "*": self.CompileCallCommand("Math.multiply", 2),
        "/": self.CompileCallCommand("Math.divide", 2)
    }
    return operator_table[op.op.symbol]

  def CompileIntegerConstant(self, integer_constant, env):
    return self.CompilePushCommand(
        "constant", int(integer_constant.integer_constant))

  def CompileStringConstant(self, string_constant, env):
    result = []
    n = len(string_constant.string_constant)
    result.extend(self.CompilePushCommand("constant", n))
    result.extend(self.CompileCallCommand("String.new", 1))
    for ch in string_constant.string_constant:
      result.extend(self.CompilePushCommand("constant", ord(ch)))
      result.extend(self.CompileCallCommand("String.appendChar", 2))
    return result

  def CompileKeywordConstant(self, keyword_constant, env):
    value = keyword_constant.constant.keyword
    if value == "true":
      result = []
      result.extend(self.CompilePushCommand("constant", 1))
      result.extend(self.CompileArithmeticCommand("neg"))
      return result
    elif value in ("false", "null"):
      return self.CompilePushCommand("constant", 0)
    elif value == "this":
      return self.CompilePushCommand("pointer", 0)

    raise CodeGenerationError("Unknown keyword constant " +
        value)

  def CompileIdentifier(self, identifier, env):
    value = env.Lookup(identifier.identifier)
    if value is None:
      raise CodeGenerationError("Unknown identifier " + identifier.identifier)

    if value[1] == "field":
      value = (value[0], "this", value[2])

    _, kind, index = value
    return self.CompilePushCommand(kind, index)

  def CompileArrayAccess(self, array_access, env):
    result = []
    result.extend(self.CompileExpression(array_access[1], env))
    result.extend(self.CompileIdentifier(array_access[0], env))
    result.extend(self.CompileArithmeticCommand("add"))
    result.extend(self.CompilePopCommand("pointer", 1))
    result.extend(self.CompilePushCommand("that", 0))
    return result

  def CompileSubroutineCall(self, call, env):
    name = call.subroutine_call.__class__.__name__
    return getattr(self, "Compile" +  name)(call.subroutine_call, env)

  def CompileFunctionSubroutineCall(self, call, env):
    result = []
    result.extend(self.CompilePushCommand("pointer", 0))
    for expression in call.expression_list:
      result.extend(self.CompileExpression(expression, env))
    result.extend(self.CompileCallCommand(
        "%s.%s" % (self.class_name.identifier, call.function_name.identifier),
        1 + len(call.expression_list)))
    return result

  def CompileMethodSubroutineCall(self, call, env):
    value = env.Lookup(call.var_name.identifier)
    if value is None:
      return self.CompileStaticMethodSubroutineCall(call, env)

    if value[1] == "field":
      value = (value[0], "this", value[2])

    result = []
    result.extend(self.CompilePushCommand(value[1], value[2]))
    for expression in call.expression_list:
      result.extend(self.CompileExpression(expression, env))
    result.extend(self.CompileCallCommand(
        "%s.%s" % (value[0], call.method_name.identifier),
        1 + len(call.expression_list)))
    return result

  def CompileStaticMethodSubroutineCall(self, call, env):
    class_name = ""
    if call.__class__.__name__ == "MethodSubroutineCall":
      class_name = call.var_name.identifier
    else:
      class_name = call.class_name.identifier

    result = []
    for expression in call.expression_list:
      result.extend(self.CompileExpression(expression, env))
    result.extend(self.CompileCallCommand(
        "%s.%s" % (class_name, call.method_name.identifier),
        len(call.expression_list)))
    return result

  def CompileUnaryOpTerm(self, term, env):
    result = []
    result.extend(self.CompileTerm(term.term, env))
    result.extend(self.CompileUnaryOperator(term.op, env))
    return result

  def CompileUnaryOperator(self, op, env):
    if op.op.symbol == "-":
      return self.CompileArithmeticCommand("neg")
    elif op.op.symbol == "~":
      return self.CompileArithmeticCommand("not")
    else:
      raise CodeGenerationError("'%s' is not a unary operator" %
          (op.op.symbol))

  def _CountLocalVariables(self, subroutine):
    cnt = 0
    for var_dec in subroutine.body.var_decs:
      cnt += len(var_dec.var_names)
    return cnt

  def _GetVarType(self, var_type):
    if var_type.__class__.__name__ == "Keyword":
      return var_type.keyword
    else:
      return var_type.identifier


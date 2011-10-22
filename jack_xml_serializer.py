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


import cgi
import os

import jack_lang_model


class JackXMLSerializer(object):

  def __init__(self):
    pass

  def Serialize(self, jack_program):
    return os.linesep.join(self.SerializeClass(jack_program))

  def SerializeKeyword(self, keyword):
    return ["<keyword>", cgi.escape(keyword), "</keyword>"]

  def SerializeSymbol(self, symbol):
    return ["<symbol>", cgi.escape(symbol), "</symbol>"]

  def SerializeIdentifier(self, identifier):
    return ["<identifier>", cgi.escape(identifier), "</identifier>"]

  def SerializeIntegerConstant(self, integer_constant):
    return ["<integerConstant>",
        integer_constant.integer_constant, "</integerConstant>"]

  def SerializeStringConstant(self, string_constant):
    return ["<stringConstant>",
        string_constant.string_constant, "</stringConstant>"]

  def SerializeKeywordConstant(self, keyword_constant):
    return self.SerializeKeyword(keyword_constant.constant.keyword)

  def SerializeClass(self, jack_class):
    result = []
    result.append("<class>")
    result.extend(self.SerializeKeyword("class"))
    result.extend(self.SerializeClassName(jack_class.class_name))
    result.extend(self.SerializeSymbol("{"))
    for class_var_dec in jack_class.class_var_decs:
      result.extend(self.SerializeClassVarDec(class_var_dec))
    for subroutine_dec in jack_class.subroutine_decs:
      result.extend(self.SerializeSubroutineDec(subroutine_dec))
    result.extend(self.SerializeSymbol("}"))
    result.append("</class>")
    return result

  def SerializeClassName(self, class_name):
    return self.SerializeIdentifier(class_name.identifier)

  def SerializeClassVarDec(self, var_dec):
    result = []
    result.append("<classVarDec>")
    result.extend(self.SerializeKeyword(var_dec.scope.keyword))
    result.extend(self.SerializeVarType(var_dec.var_type))
    result.extend(self.SerializeVarName(var_dec.var_names[0]))
    for var_name in var_dec.var_names[1:]:
      result.extend(self.SerializeSymbol(","))
      result.extend(self.SerializeVarName(var_name))
    result.extend(self.SerializeSymbol(";"))
    result.append("</classVarDec>")
    return result

  def SerializeSubroutineDec(self, subroutine_dec):
    result = []
    result.append("<subroutineDec>")
    result.extend(
        self.SerializeKeyword(subroutine_dec.subroutine_type.keyword))
    if subroutine_dec.return_type.__class__.__name__ == "Keyword":
      result.extend(self.SerializeKeyword(subroutine_dec.return_type.keyword))
    else:
      result.extend(self.SerializeVarType(subroutine_dec.return_type))
    result.extend(self.SerializeSubroutineName(subroutine_dec.name))
    result.extend(self.SerializeSymbol("("))
    result.extend(self.SerializeParameterList(subroutine_dec.param_list))
    result.extend(self.SerializeSymbol(")"))
    result.extend(self.SerializeSubroutineBody(subroutine_dec.body))
    result.append("</subroutineDec>")
    return result

  def SerializeVarType(self, var_type):
    if var_type.var_type.__class__.__name__ == "Keyword":
      return self.SerializeKeyword(var_type.var_type.keyword)
    else:
      return self.SerializeClassName(var_type.var_type)

  def SerializeVarName(self, var_name):
    return self.SerializeIdentifier(var_name.identifier)

  def SerializeSubroutineName(self, subroutine_name):
    return self.SerializeIdentifier(subroutine_name.identifier)

  def SerializeParameterList(self, param_list):
    result = []
    result.append("<parameterList>")
    if len(param_list) > 0:
      result.extend(self.SerializeVarType(param_list[0][0]))
      result.extend(self.SerializeVarName(param_list[0][1]))
    if len(param_list) > 1:
      for var_type, var_name in param_list[1:]:
        result.extend(self.SerializeSymbol(","))
        result.extend(self.SerializeVarType(var_type))
        result.extend(self.SerializeVarName(var_name))
    result.append("</parameterList>")
    return result

  def SerializeSubroutineBody(self, body):
    result = []
    result.append("<subroutineBody>")
    result.extend(self.SerializeSymbol("{"))
    for var_dec in body.var_decs:
      result.extend(self.SerializeVarDec(var_dec))
    result.extend(self.SerializeStatements(body.statements))
    result.extend(self.SerializeSymbol("}"))
    result.append("</subroutineBody>")
    return result

  def SerializeVarDec(self, var_dec):
    result = []
    result.append("<varDec>")
    result.extend(self.SerializeKeyword("var"))
    result.extend(self.SerializeVarType(var_dec.var_type))
    result.extend(self.SerializeVarName(var_dec.var_names[0]))
    for var_name in var_dec.var_names[1:]:
      result.extend(self.SerializeSymbol(","))
      result.extend(self.SerializeVarName(var_name))
    result.extend(self.SerializeSymbol(";"))
    result.append("</varDec>")
    return result

  def SerializeStatements(self, statements):
    result = []
    result.append("<statements>")
    for statement in statements.statements:
      result.extend(self.SerializeStatement(statement))
    result.append("</statements>")
    return result

  def SerializeStatement(self, statement):
    name = statement.statement.__class__.__name__
    return getattr(self, "Serialize" + name)(statement.statement)

  def SerializeLetStatement(self, statement):
    result = []
    result.append("<letStatement>")
    result.extend(self.SerializeKeyword("let"))
    name = statement.let_statement.__class__.__name__
    result.extend(getattr(self, "Serialize" + name)(statement.let_statement))
    result.append("</letStatement>")
    return result

  def SerializeRegularLetStatement(self, statement):
    result = []
    result.extend(self.SerializeVarName(statement.var_name))
    result.extend(self.SerializeSymbol("="))
    result.extend(self.SerializeExpression(statement.expression))
    result.extend(self.SerializeSymbol(";"))
    return result

  def SerializeArrayLetStatement(self, statement):
    result = []
    result.extend(self.SerializeVarName(statement.var_name))
    result.extend(self.SerializeSymbol("["))
    result.extend(self.SerializeExpression(statement.index_expression))
    result.extend(self.SerializeSymbol("]"))
    result.extend(self.SerializeSymbol("="))
    result.extend(self.SerializeExpression(statement.expression))
    result.extend(self.SerializeSymbol(";"))
    return result

  def SerializeIfStatement(self, statement):
    result = []
    result.append("<ifStatement>")
    result.extend(self.SerializeKeyword("if"))
    name = statement.if_statement.__class__.__name__
    result.extend(getattr(self, "Serialize" + name)(statement.if_statement))
    result.append("</ifStatement>")
    return result

  def SerializeRegularIfStatement(self, statement):
    result = []
    result.extend(self.SerializeSymbol("("))
    result.extend(self.SerializeExpression(statement.expression))
    result.extend(self.SerializeSymbol(")"))
    result.extend(self.SerializeSymbol("{"))
    result.extend(self.SerializeStatements(statement.statements))
    result.extend(self.SerializeSymbol("}"))
    return result

  def SerializeIfElseStatement(self, statement):
    result = []
    result.extend(self.SerializeSymbol("("))
    result.extend(self.SerializeExpression(statement.expression))
    result.extend(self.SerializeSymbol(")"))
    result.extend(self.SerializeSymbol("{"))
    result.extend(self.SerializeStatements(statement.if_statements))
    result.extend(self.SerializeSymbol("}"))
    result.extend(self.SerializeKeyword("else"))
    result.extend(self.SerializeSymbol("{"))
    result.extend(self.SerializeStatements(statement.else_statements))
    result.extend(self.SerializeSymbol("}"))
    return result

  def SerializeWhileStatement(self, statement):
    result = []
    result.append("<whileStatement>")
    result.extend(self.SerializeKeyword("while"))
    result.extend(self.SerializeSymbol("("))
    result.extend(self.SerializeExpression(statement.expression))
    result.extend(self.SerializeSymbol(")"))
    result.extend(self.SerializeSymbol("{"))
    result.extend(self.SerializeStatements(statement.statements))
    result.extend(self.SerializeSymbol("}"))
    result.append("</whileStatement>")
    return result

  def SerializeDoStatement(self, statement):
    result = []
    result.append("<doStatement>")
    result.extend(self.SerializeKeyword("do"))
    result.extend(self.SerializeSubroutineCall(statement.subroutine_call))
    result.extend(self.SerializeSymbol(";"))
    result.append("</doStatement>")
    return result

  def SerializeReturnStatement(self, statement):
    result = []
    result.append("<returnStatement>")
    name = statement.return_statement.__class__.__name__
    result.extend(
        getattr(self, "Serialize" + name)(statement.return_statement))
    result.append("</returnStatement>")
    return result

  def SerializeExpressionReturnStatement(self, statement):
    result = []
    result.extend(self.SerializeKeyword("return"))
    result.extend(self.SerializeExpression(statement.expression))
    result.extend(self.SerializeSymbol(";"))
    return result

  def SerializeNoExpressionReturnStatement(self, statement):
    result = []
    result.extend(self.SerializeKeyword("return"))
    result.extend(self.SerializeSymbol(";"))
    return result

  def SerializeExpression(self, expression):
    result = []
    result.append("<expression>")
    result.extend(self.SerializeTerm(expression.first_term))
    for op, term in expression.op_term_list:
      result.extend(self.SerializeOperator(op))
      result.extend(self.SerializeTerm(term))
    result.append("</expression>")
    return result

  def SerializeTerm(self, term):
    result = []
    result.append("<term>")
    name = term.term.__class__.__name__
    if name in [
        "IntegerConstant",
        "StringConstant",
        "KeywordConstant",
        "SubroutineCall",
        "UnaryOpTerm"]:
      result.extend(getattr(self, "Serialize" + name)(term.term))
    elif name == "tuple":
      result.extend(self.SerializeVarName(term.term[0]))
      result.extend(self.SerializeSymbol("["))
      result.extend(self.SerializeExpression(term.term[1]))
      result.extend(self.SerializeSymbol("]"))
    elif name == "Identifier":
      result.extend(self.SerializeIdentifier(term.term.identifier))
    elif name == "Expression":
      result.extend(self.SerializeSymbol("("))
      result.extend(self.SerializeExpression(term.term))
      result.extend(self.SerializeSymbol(")"))
    result.append("</term>")
    return result

  def SerializeUnaryOpTerm(self, term):
    result = []
    result.extend(self.SerializeUnaryOperator(term.op))
    result.extend(self.SerializeTerm(term.term))
    return result

  def SerializeOperator(self, op):
    return self.SerializeSymbol(op.op.symbol)

  def SerializeSubroutineCall(self, call):
    name = call.subroutine_call.__class__.__name__
    return getattr(self, "Serialize" + name)(call.subroutine_call)

  def SerializeFunctionSubroutineCall(self, call):
    result = []
    result.extend(self.SerializeSubroutineName(call.function_name))
    result.extend(self.SerializeSymbol("("))
    result.extend(self.SerializeExpressionList(call.expression_list))
    result.extend(self.SerializeSymbol(")"))
    return result

  def SerializeMethodSubroutineCall(self, call):
    result = []
    result.extend(self.SerializeVarName(call.var_name))
    result.extend(self.SerializeSymbol("."))
    result.extend(self.SerializeSubroutineName(call.method_name))
    result.extend(self.SerializeSymbol("("))
    result.extend(self.SerializeExpressionList(call.expression_list))
    result.extend(self.SerializeSymbol(")"))
    return result

  def SerializeStaticMethodSubroutineCall(self, call):
    result = []
    result.extend(self.SerializeClassName(call.class_name))
    result.extend(self.SerializeSymbol("."))
    result.extend(self.SerializeSubroutineName(call.method_name))
    result.extend(self.SerializeSymbol("("))
    result.extend(self.SerializeExpressionList(call.expression_list))
    result.extend(self.SerializeSymbol(")"))
    return result

  def SerializeExpressionList(self, expression_list):
    result = []
    result.append("<expressionList>")
    if len(expression_list) > 0:
      result.extend(self.SerializeExpression(expression_list[0]))
    if len(expression_list) > 1:
      for expression in expression_list[1:]:
        result.extend(self.SerializeSymbol(","))
        result.extend(self.SerializeExpression(expression))
    result.append("</expressionList>")
    return result

  def SerializeUnaryOperator(self, op):
    return self.SerializeSymbol(op.op.symbol)


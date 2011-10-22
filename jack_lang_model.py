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


class Keyword(object):
  def __init__(self, keyword):
    self.keyword = keyword


class Symbol(object):
  def __init__(self, symbol):
    self.symbol = symbol


class IntegerConstant(object):
  def __init__(self, integer_constant):
    self.integer_constant = integer_constant


class StringConstant(object):
  def __init__(self, string_constant):
    self.string_constant = string_constant


class Identifier(object):
  def __init__(self, identifier):
    self.identifier = identifier


class Class(object):
  def __init__(self, class_name, class_var_decs, subroutine_decs):
    self.class_name = class_name
    self.class_var_decs = class_var_decs
    self.subroutine_decs = subroutine_decs


class ClassVarDec(object):
  def __init__(self, scope, var_type, var_names):
    self.scope = scope
    self.var_type = var_type
    self.var_names = var_names


class VarType(object):
  def __init__(self, var_type):
    self.var_type = var_type


class SubroutineDec(object):
  def __init__(self, subroutine_type, return_type, name, param_list, body):
    self.subroutine_type = subroutine_type
    self.return_type = return_type
    self.name = name
    self.param_list = param_list
    self.body = body


class SubroutineBody(object):
  def __init__(self, var_decs, statements):
    self.var_decs = var_decs
    self.statements = statements


class VarDec(object):
  def __init__(self, var_type, var_names):
    self.var_type = var_type
    self.var_names = var_names


class ClassName(object):
  def __init__(self, identifier):
    self.identifier = identifier


class SubroutineName(object):
  def __init__(self, identifier):
    self.identifier = identifier


class VarName(object):
  def __init__(self, identifier):
    self.identifier = identifier


class Statements(object):
  def __init__(self, statements):
    self.statements = statements


class Statement(object):
  def __init__(self, statement):
    self.statement = statement


class LetStatement(object):
  def __init__(self, let_statement):
    self.let_statement = let_statement


class RegularLetStatement(object):
  def __init__(self, var_name, expression):
    self.var_name = var_name
    self.expression = expression


class ArrayLetStatement(object):
  def __init__(self, var_name, index_expression, expression):
    self.var_name = var_name
    self.index_expression = index_expression
    self.expression = expression


class IfStatement(object):
  def __init__(self, if_statement):
    self.if_statement = if_statement


class RegularIfStatement(object):
  def __init__(self, expression, statements):
    self.expression = expression
    self.statements = statements


class IfElseStatement(object):
  def __init__(self, expression, if_statements, else_statements):
    self.expression = expression
    self.if_statements = if_statements
    self.else_statements = else_statements


class WhileStatement(object):
  def __init__(self, expression, statements):
    self.expression = expression
    self.statements = statements


class DoStatement(object):
  def __init__(self, subroutine_call):
    self.subroutine_call = subroutine_call


class ReturnStatement(object):
  def __init__(self, return_statement):
    self.return_statement = return_statement


class ExpressionReturnStatement(object):
  def __init__(self, expression):
    self.expression = expression


class NoExpressionReturnStatement(object):
  def __init__(self):
    pass


class Expression(object):
  def __init__(self, first_term, op_term_list):
    self.first_term = first_term
    self.op_term_list = op_term_list


class Term(object):
  def __init__(self, term):
    self.term = term


class UnaryOpTerm(object):
  def __init__(self, op, term):
    self.op = op
    self.term = term


class SubroutineCall(object):
  def __init__(self, subroutine_call):
    self.subroutine_call = subroutine_call


class FunctionSubroutineCall(object):
  def __init__(self, function_name, expression_list):
    self.function_name = function_name
    self.expression_list = expression_list


class MethodSubroutineCall(object):
  def __init__(self, var_name, method_name, expression_list):
    self.var_name = var_name
    self.method_name = method_name
    self.expression_list = expression_list


class StaticMethodSubroutineCall(object):
  def __init__(self, class_name, method_name, expression_list):
    self.class_name = class_name
    self.method_name = method_name
    self.expression_list = expression_list


class Operator(object):
  def __init__(self, op):
    self.op = op


class UnaryOperator(object):
  def __init__(self, op):
    self.op = op


class KeywordConstant(object):
  def __init__(self, constant):
    self.constant = constant



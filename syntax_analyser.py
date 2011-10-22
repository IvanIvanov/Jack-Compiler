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

import jack_lang_model


jlm = jack_lang_model


class SyntacticError(Exception):
  def __init__(self, message):
    self.message = message


class SyntaxAnalyser(object):

  _GRAMMAR = [
      ("Class", ["sequence", "keywordclass", "ClassName", "symbol{", 
                 "ClassVarDecs", "SubroutineDecs", "symbol}"],
       lambda res: jlm.Class(res[2], res[4], res[5])),
      ("ClassVarDecs", ["star", "ClassVarDec"],
       lambda res: res[1:]),
      ("SubroutineDecs", ["star", "SubroutineDec"],
       lambda res: res[1:]),
      ("ClassVarDec", ["sequence", "DecScope", "Type", "VarName",
                       "CommaPrecededVarNames", "symbol;"],
       lambda res: jlm.ClassVarDec(res[1], res[2], [res[3]] + res[4])),
      ("DecScope", ["choice", "keywordstatic", "keywordfield"],
       lambda res: res[1]),
      ("CommaPrecededVarNames", ["star", "CommaPrecededVarName"],
       lambda res: res[1:]),
      ("CommaPrecededVarName", ["sequence", "symbol,", "VarName"],
       lambda res: res[2]),
      ("Type", ["choice", "keywordint", "keywordchar", "keywordboolean",
                "ClassName"],
       lambda res: jlm.VarType(res[1])),
      ("SubroutineDec", ["sequence", "SubroutineType", "SubroutineReturnType",
                         "SubroutineName", "symbol(", "ParameterList",
                         "symbol)", "SubroutineBody"],
       lambda res: jlm.SubroutineDec(res[1], res[2], res[3], res[5], res[7])),
      ("SubroutineType", ["choice", "keywordconstructor", "keywordfunction",
                          "keywordmethod"],
       lambda res: res[1]),
      ("SubroutineReturnType", ["choice", "keywordvoid", "Type"],
       lambda res: res[1]),
      ("ParameterList", ["question", "NonemptyParameterList"],
       lambda res: res[1] if len(res) > 1 else []),
      ("NonemptyParameterList", ["sequence", "Type", "VarName",
                                 "CommaPrecededTypedVarNames"],
       lambda res: [(res[1], res[2])] + res[3]),
      ("CommaPrecededTypedVarNames", ["star", "CommaPrecededTypedVarName"],
       lambda res: res[1:]),
      ("CommaPrecededTypedVarName", ["sequence", "symbol,", "Type", "VarName"],
       lambda res: (res[2], res[3])),
      ("SubroutineBody", ["sequence", "symbol{", "VarDecs", "Statements",
                          "symbol}"],
       lambda res: jlm.SubroutineBody(res[2], res[3])),
      ("VarDecs", ["star", "VarDec"],
       lambda res: res[1:]),
      ("VarDec", ["sequence", "keywordvar", "Type", "VarName", 
                  "CommaPrecededVarNames", "symbol;"], 
       lambda res: jlm.VarDec(res[2], [res[3]] + res[4])),
      ("ClassName", ["sequence", "Identifier"], 
       lambda res: res[1]),
      ("SubroutineName", ["sequence", "Identifier"], 
       lambda res: res[1]),
      ("VarName", ["sequence", "Identifier"], 
       lambda res: res[1]),
      ("Statements", ["star", "Statement"], 
       lambda res: jlm.Statements(res[1:])),
      ("Statement", ["choice", "LetStatement", "IfStatement", "DoStatement",
                     "WhileStatement", "ReturnStatement"], 
       lambda res: jlm.Statement(res[1])),
      ("LetStatement", ["choice", "RegularLetStatement", "ArrayLetStatement"],
       lambda res: jlm.LetStatement(res[1])),
      ("RegularLetStatement", ["sequence", "keywordlet", "VarName", "symbol=",
                               "Expression", "symbol;"], 
       lambda res: jlm.RegularLetStatement(res[2], res[4])),
      ("ArrayLetStatement", ["sequence", "keywordlet", "ArrayVarName",
                             "symbol=", "Expression", "symbol;"],
       lambda res: jlm.ArrayLetStatement(res[2][0], res[2][1], res[4])),
      ("IfStatement", ["choice", "IfElseStatement", "RegularIfStatement"],
       lambda res: jlm.IfStatement(res[1])),
      ("RegularIfStatement", ["sequence", "keywordif", "symbol(",
                              "Expression", "symbol)", "symbol{",
                              "Statements", "symbol}"], 
       lambda res: jlm.RegularIfStatement(res[3], res[6])),
      ("IfElseStatement", ["sequence", "RegularIfStatement", "keywordelse",
                           "symbol{", "Statements", "symbol}"],
       lambda res: jlm.IfElseStatement(res[1].expression,
                                       res[1].statements, res[4])),
      ("WhileStatement", ["sequence", "keywordwhile", "symbol(", "Expression",
                          "symbol)", "symbol{", "Statements", "symbol}"],
       lambda res: jlm.WhileStatement(res[3], res[6])),
      ("DoStatement", ["sequence", "keyworddo", "SubroutineCall", "symbol;"],
       lambda res: jlm.DoStatement(res[2])),
      ("ReturnStatement", ["choice", "ExpressionReturnStatement",
                           "NoExpressionReturnStatement"], 
       lambda res: jlm.ReturnStatement(res[1])),
      ("ExpressionReturnStatement", ["sequence", "keywordreturn", "Expression",
                                     "symbol;"], 
       lambda res: jlm.ExpressionReturnStatement(res[2])),
      ("NoExpressionReturnStatement", ["sequence", "keywordreturn",
                                       "symbol;"], 
       lambda res: jlm.NoExpressionReturnStatement()),
      ("Expression", ["sequence", "Term", "OpTerms"], 
       lambda res: jlm.Expression(res[1], res[2])),
      ("OpTerms", ["star", "OpTerm"], 
       lambda res: res[1:]),
      ("OpTerm", ["sequence", "Op", "Term"], 
       lambda res: (res[1], res[2])),
      ("Term", ["choice", "IntegerConstant", "KeywordConstant",
                "StringConstant", "SubroutineCall", "ArrayVarName",
                "VarName", "ParenExpression", "UnaryOpTerm"],
       lambda res: jlm.Term(res[1])),
      ("ArrayVarName", ["sequence", "VarName", "symbol[", "Expression",
                        "symbol]"], 
       lambda res: (res[1], res[3])),
      ("ParenExpression", ["sequence", "symbol(", "Expression",
                           "symbol)"], 
       lambda res: res[2]),
      ("UnaryOpTerm", ["sequence", "UnaryOp", "Term"], 
       lambda res: jlm.UnaryOpTerm(res[1], res[2])),
      ("SubroutineCall", ["choice", "FunctionCall", "MethodCall",
                          "StaticMethodCall"], 
       lambda res: jlm.SubroutineCall(res[1])),
      ("FunctionCall", ["sequence", "SubroutineName", "symbol(",
                        "ExpressionList", "symbol)"], 
       lambda res: jlm.FunctionSubroutineCall(res[1], res[3])),
      ("MethodCall", ["sequence", "VarName", "symbol.", "SubroutineName",
                      "symbol(", "ExpressionList", "symbol)"],
       lambda res: jlm.MethodSubroutineCall(res[1], res[3], res[5])),
      ("StaticMethodCall", ["sequence", "ClassName", "symbol.",
                            "SubroutineName", "symbol(", "ExpressionList",
                            "symbol)"], 
       lambda res: jlm.StaticMethodSubroutineCall(res[1], res[3], res[5])),
      ("ExpressionList", ["question", "NonemptyExpressionList"],
       lambda res: res[1] if len(res) > 1 else []),
      ("NonemptyExpressionList", ["sequence", "Expression", 
                                  "CommaPrecededExpressions"],
       lambda res: [res[1]] + res[2]),
      ("CommaPrecededExpressions", ["star", "CommaPrecededExpression"],
       lambda res: res[1:]),
      ("CommaPrecededExpression", ["sequence", "symbol,", "Expression"],
       lambda res: res[2]),
      ("Op", ["choice", "symbol+", "symbol-", "symbol*", "symbol/",
              "symbol&", "symbol|", "symbol<", "symbol>", "symbol="],
       lambda res: jlm.Operator(res[1])),
      ("UnaryOp", ["choice", "symbol-", "symbol~"], 
       lambda res: jlm.UnaryOperator(res[1])),
      ("KeywordConstant", ["choice", "keywordtrue", "keywordfalse",
                           "keywordnull", "keywordthis"], 
       lambda res: jlm.KeywordConstant(res[1]))
  ]

  def __init__(self, tokens):
    self.n = len(tokens)
    self.tokens = tokens
    for rule in self._GRAMMAR:
      function = getattr(self, "Generate%sParser" % (rule[1][0].capitalize(),))
      function(rule[0], rule[1][1:], rule[2])

  @staticmethod
  def Parse(tokens):
    syntax_analyser = SyntaxAnalyser(tokens)
    parser = getattr(syntax_analyser, "ParseClass")
    result, index = parser(0)
    if index < len(tokens):
      raise SyntacticError("Unparsed tokens left.")
    else:
      return result

  def CallParser(self, parser_name, index):
    if parser_name.startswith("keyword"):
      return self.ParseKeyword(parser_name[7:], index)
    elif parser_name.startswith("symbol"):
      return self.ParseSymbol(parser_name[6:], index)
    else:
      return getattr(self, "Parse" + parser_name)(index)

  def GenerateSequenceParser(self, name, sequence, constructor):
    def Parser(self, index):
      try:
        i = index
        result = []
        result.append(name)
        for parser_name in sequence:
          res, i = self.CallParser(parser_name, i)
          result.append(res)
        return constructor(result), i
      except SyntacticError as error:
        raise SyntacticError("Can't parse " +
            name + os.linesep + error.message)
    setattr(SyntaxAnalyser, "Parse" + name, Parser)

  def GenerateChoiceParser(self, name, choice, constructor):
    def Parser(self, index):
      i = index
      for parser_name in choice:
        try:
          res, i = self.CallParser(parser_name, i)
          return constructor([name, res]), i
        except SyntacticError as error:
          pass
      raise SyntacticError("Can't parse " + name)
    setattr(SyntaxAnalyser, "Parse" + name, Parser)

  def GenerateStarParser(self, name, thing, constructor):
    def Parser(self, index):
      i = index
      result = []
      result.append(name)
      try:
        while True:
          res, i = self.CallParser(thing[0], i)
          result.append(res)
      except SyntacticError as error:
        return constructor(result), i
    setattr(SyntaxAnalyser, "Parse" + name, Parser)

  def GenerateQuestionParser(self, name, thing, constructor):
    def Parser(self, index):
      i = index
      result = []
      result.append(name)
      try:
        res, i = self.CallParser(thing[0], i)
        result.append(res)
        return constructor(result), i
      except SyntacticError as error:
        return constructor(result), i
    setattr(SyntaxAnalyser, "Parse" + name, Parser)

  def ParseKeyword(self, keyword, index):
    token = self._NextToken(index)
    if (token and token.__class__.__name__ == "Keyword" and
        token.keyword == keyword):
      return jack_lang_model.Keyword(keyword), index + 1
    else:
      raise SyntacticError("Can't parse keyword: %s" % (keyword,))

  def ParseSymbol(self, symbol, index):
    token = self._NextToken(index)
    if (token and token.__class__.__name__ == "Symbol" and
        token.symbol == symbol):
      return jack_lang_model.Symbol(symbol), index + 1
    else:
      raise SyntacticError("Can't parse symbol: %s" % (symbol,))

  def ParseIntegerConstant(self, index):
    token = self._NextToken(index)
    if token and token.__class__.__name__ == "IntegerConstant":
      return jack_lang_model.IntegerConstant(token.integer_constant), index + 1
    else:
      raise SyntacticError("Can't parse integer constant")

  def ParseStringConstant(self, index):
    token = self._NextToken(index)
    if token and token.__class__.__name__ == "StringConstant":
      return jack_lang_model.StringConstant(token.string_constant), index + 1
    else:
      raise SyntacticError("Can't parse string constant")

  def ParseIdentifier(self, index):
    token = self._NextToken(index)
    if token and token.__class__.__name__ == "Identifier":
      return jack_lang_model.Identifier(token.identifier), index + 1
    else:
      raise SyntacticError("Can't parse identifier")

  def _NextToken(self, index):
    return self.tokens[index] if index < self.n else None


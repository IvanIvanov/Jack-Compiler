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
import re
import jack_lang_model


class LexicalError(Exception):
  def __init__(self, message):
    self.message = message


class LexicalAnalyser(object):
  
  _RE_KEYWORD = re.compile(
      r"(?:"
      r"class|constructor|function|method|"
      r"field|static|var|int|char|boolean|"
      r"void|true|false|null|this|let|do|"
      r"if|else|while|return"
      r")(?=[^a-zA-Z0-9_])")

  _RE_SYMBOL = re.compile("[%s]" % (re.escape(r"{}()[].,;+-*/&|<>=~")))

  _RE_INTEGER_CONSTANT = re.compile(r"\d+")

  _RE_STRING_CONSTANT = re.compile(r"\"[^\"\r\n]*\"")

  _RE_IDENTIFIER = re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*")

  _RE_WHITESPACE = re.compile(r"\s")

  _RE_COMMENT_1 = re.compile(r"//[^\n\r]*[^\n\r]")

  _RE_COMMENT_2 = re.compile(r"/\*.*?\*/", re.DOTALL)

  _RE_END_OF_LINE = re.compile(r"[^\n\r]*")

  _TOKEN_MATCHING_TABLE = [
      (_RE_WHITESPACE, None),
      (_RE_COMMENT_1, None),
      (_RE_COMMENT_2, None),
      (_RE_KEYWORD, jack_lang_model.Keyword),
      (_RE_SYMBOL, jack_lang_model.Symbol),
      (_RE_INTEGER_CONSTANT, jack_lang_model.IntegerConstant),
      (_RE_STRING_CONSTANT, jack_lang_model.StringConstant),
      (_RE_IDENTIFIER, jack_lang_model.Identifier)
  ]

  @staticmethod
  def Tokenize(program):
    pos = 0
    lines = 0
    n = len(program)
    tokens = []

    while pos < n:
      match = None
      token = None
      for regex, constructor in LexicalAnalyser._TOKEN_MATCHING_TABLE:
        match = regex.match(program, pos)
        if match:
          if constructor: token = constructor(match.group(0).replace("\"", ""))
          break
      if match:
        pos += len(match.group(0))
        lines += match.group(0).count(os.linesep)
        if token: tokens.append(token)
      else:
        raise LexicalError("Lexical Error on line %d: %s" % (
            lines + 1,
            LexicalAnalyser._RE_END_OF_LINE.match(program, pos).group(0)))

    return tokens


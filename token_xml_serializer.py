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


class TokenXMLSerializer(object):

  @staticmethod
  def SerializeToXML(tokens):
    result = []
    result.append("<tokens>")
    for token in tokens:
      if token.__class__.__name__ == "Keyword":
        result.append("<keyword>%s</keyword>" % (cgi.escape(token.keyword),))
      elif token.__class__.__name__ == "Symbol":
        result.append("<symbol>%s</symbol>" % (cgi.escape(token.symbol),))
      elif token.__class__.__name__ == "IntegerConstant":
        result.append("<integerConstant>%s</integerConstant>" % (
            cgi.escape(token.integer_constant),))
      elif token.__class__.__name__ == "StringConstant":
        result.append("<stringConstant>%s</stringConstant>" % (
            cgi.escape(token.string_constant),))
      elif token.__class__.__name__ == "Identifier":
        result.append("<identifier>%s</identifier>" % (
            cgi.escape(token.identifier),))
    result.append("</tokens>")
    return os.linesep.join(result)


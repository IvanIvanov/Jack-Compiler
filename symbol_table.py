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


class SymbolTable(object):
  
  def __init__(self, parent):
    self.parent = parent
    self.table = {}

  def Lookup(self, name):
    if name in self.table:
      return self.table[name]
    elif self.parent:
      return self.parent.Lookup(name)
    else:
      return None

  def Insert(self, name, entry_type, entry_kind):
    index = self.CountKindLocal(entry_kind)
    self.table[name] = (entry_type, entry_kind, index)

  def CountKind(self, entry_kind):
    cnt = self.CountKindLocal(entry_kind)
    if self.parent:
      return cnt + self.parent.CountKind(entry_kind)
    else:
      return cnt

  def CountKindLocal(self, entry_kind):
    cnt = 0
    for _, (_, kind, _) in self.table.items():
      if kind == entry_kind:
        cnt += 1
    return cnt


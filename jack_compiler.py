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
import sys

import jack_to_vm_compiler
import lexical_analyser
import syntax_analyser


def CompileFile(file_name):
  try:
    with open(file_name, "r") as program_file:
      program = "".join(program_file.readlines())
      tokens = lexical_analyser.LexicalAnalyser.Tokenize(program)
      tree = syntax_analyser.SyntaxAnalyser.Parse(tokens)
      compiler = jack_to_vm_compiler.JackToVMCompiler()
      serialized_program = compiler.CompileVMCode(tree)
      with open(file_name[:-4] + "vm", "w") as output_file:
        output_file.write(serialized_program)
  except lexical_analyser.LexicalError as error:
    print error.messagei
  except syntax_analyser.SyntacticError as error:
    print error.message
  except jack_to_vm_compiler.CodeGenerationError as error:
    print error.message
  except IOError as error:
    print error


def main():
  if len(sys.argv) != 2:
    print "Please enter the name of a file or directory which to compile."
    return

  if not os.path.exists(sys.argv[1]):
    print "Argument is not a valid file or directory."
    return

  if os.path.isdir(sys.argv[1]):
    for file_name in os.listdir(sys.argv[1]):
      if file_name.endswith(".jack"):
        CompileFile(file_name)
  elif os.path.isfile(sys.argv[1]):
    file_name = sys.argv[1]
    if file_name.endswith(".jack"):
      CompileFile(file_name)


if __name__ == "__main__":
  main()


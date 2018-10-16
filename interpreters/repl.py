#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
import sys

from asts.null_stmnt import NullStmnt
from environment import Environment
from excepts import PimbaError
from excepts import PimbaParseError
from lexer import Lexer
from natives import Natives
from interpreters.pimba_interpreter import PimbaInterpreter
from parsers.pimba_parser import PimbaParser
from pimba_token import Token


class REPL(PimbaInterpreter):
    def __init__(self):
        self.lexer = None
        self.parser = PimbaParser()
        self.env = Natives(self).environment(Environment())

    def run(self, characters):
        try:
            self.lexer = Lexer(characters)
            while self.lexer.peek(0) != Token.EOF:
                astree = self.parser.parse(self.lexer)
                if not isinstance(astree, NullStmnt):
                    result = astree.eval(self.env)
            if result:
                print "=> " + str(result)
        except PimbaError, e:
            sys.stderr.write("PimbaError: " + str(e) + "\n")
        except PimbaParseError, e:
            sys.stderr.write("PimbaParseError: " + str(e) + "\n")
        except Exception, e:
            sys.stderr.write("PimbaNativeError: " + str(e) + "\n")

    def __call__(self, characters):
        self.run(characters)

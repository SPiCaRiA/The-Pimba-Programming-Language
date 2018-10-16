#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.null_stmnt import NullStmnt
from environment import Environment
from excepts import PimbaError
from excepts import PimbaParseError
from lexer import Lexer
from natives import Natives
from pimba_token import Token
from parsers.pimba_parser import PimbaParser
import sys


class PimbaInterpreter(object):
    def __init__(self, characters):
        self.lexer = Lexer(characters)
        self.parser = PimbaParser()
        self.env = Natives(self).environment(Environment())

    def run(self):
        try:
            while self.lexer.peek(0) != Token.EOF:
                astree = self.parser.parse(self.lexer)
                if not isinstance(astree, NullStmnt):
                    astree.eval(self.env)
        except PimbaError, e:
            sys.stderr.write("PimbaError: " + str(e) + "\n")
        except PimbaParseError, e:
            sys.stderr.write("PimbaParseError: " + str(e) + "\n")
        except Exception, e:
            sys.stderr.write("PimbaNativeError: " + str(e))

    def test(self):
        try:
            while self.lexer.peek(0) != Token.EOF:
                astree = self.parser.parse(self.lexer)
                if not isinstance(astree, NullStmnt):
                    astree.eval(self.env)
        except PimbaError, e:
            sys.stderr.write("PimbaError: " + str(e) + "\n")
        except PimbaParseError, e:
            sys.stderr.write("PimbaParseError: " + str(e) + "\n")
        except Exception, e:
            sys.stderr.write("PimbaNativeError" + str(e) + "\n")

    def __call__(self):
        self.run()

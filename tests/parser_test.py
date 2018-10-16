#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from lexer import Lexer
from parsers.pimba_parser import PimbaParser
from pimba_token import Token


def test_parser(characters):
    lexer = Lexer(characters)
    parser = PimbaParser()
    while lexer.peek(0) != Token.EOF:
        astree = parser.parse(lexer)
        print "=> " + str(astree)


if __name__ == "__main__":
    test_characters = """even = 0
odd = 0
i = 1
while i < 10 {
    if i % 2 == 0 {              // even number?
        even = even + i
    } else {
        odd = odd + i
    }
    i = i + 1
}
even + odd"""
    test_characters = """def f(int) {
    int + 1
}"""
    test_parser(test_characters)



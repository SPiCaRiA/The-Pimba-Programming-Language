#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
import re
import sys
from excepts import PimbaParseError
from pimba_token import Token
from pimba_token import StrToken
from pimba_token import NumToken
from pimba_token import IdToken


class Lexer(object):
    def __init__(self, characters):
        self.characters = isinstance(characters, list) and characters or characters.split("\n")
        self.queue = []
        punct = r"!|\"|#|$|%|&|'|\(|\)|\*|\+|,|\-|.|/|:|;|<|=|>|\?|@|[|\|]|^|_|`|{|\||}|~"
        self.regex_pattern = r'\s*((//.*)|([0-9]+)|("("|\\\\|\\n|[^"])*?")|[A-Za-z][A-Za-z0-9]*|==|>=|<=|&&|\|\||\+=|-' \
                             r'=|%s)' % punct
        self.regex = re.compile(self.regex_pattern)

        self.line_number = 0
        self.has_more = True

    def read(self):
        if self._fill_queue(0):
            return self.queue.pop(0)
        else:
            return Token.EOF

    def peek(self, index):
        if self._fill_queue(index):
            return self.queue[index]
        else:
            return Token.EOF

    def _fill_queue(self, index):
        while index >= len(self.queue):
            if self.has_more:
                self._read_line()
            else:
                return False
        return True

    def _read_line(self):
        line = self.line_number < len(self.characters) and self.characters[self.line_number] or None
        if not line:
            self.has_more = False
            return
        self.line_number += 1

        pos = 0
        end_pos = len(line)
        while pos < end_pos:
            match = self.regex.match(line, pos, end_pos)
            if match:
                self._add_token(match)
                pos = match.end(0)
            else:
                raise PimbaParseError("bad token at line " + self.line_number)
        self.queue.append(IdToken(self.line_number, Token.EOL))

    def _add_token(self, match):
        result = match.group(1)
        if result:  # if not space
            if not match.group(2):  # if not comment
                if match.group(3):
                    token = NumToken(self.line_number, int(result))
                elif match.group(4):
                    token = StrToken(self.line_number, self._to_string_literal(result))
                else:
                    token = IdToken(self.line_number, result)
                self.queue.append(token)

    @staticmethod
    def _to_string_literal(string):
        return string.replace(r"\n", "\n").replace("\\\"", "\"").replace(r"\\", "\\").replace(r'"', "")

    def __call__(self):
        self.read()


def main(file_name):
    if not file_name:
        file_name = raw_input("Input Filename: ")
    characters = ""

    try:
        with open(file_name, "r") as _file:
            for each_line in _file:
                characters += each_line
    except IOError:
        sys.stderr.write("Cannot open file <%s> - lexer.py/main()" % file_name)

    lexer = Lexer(characters)
    result = lexer()
    while result != Token.EOF:
        print "=>" + result


if __name__ == "__main__":
    main("")

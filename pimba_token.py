#!/usr/bin/python
# -*-coding=utf8-*-

from __future__ import absolute_import
from excepts import PimbaError


class Token(object):
    EOF = None
    EOL = r"\n"

    def __init__(self, line_number):
        self.line_number = line_number

    def is_identifier(self):
        return False

    def is_number(self):
        return False

    def is_string(self):
        return False

    def get_line_number(self):
        return self.line_number

    def get_number(self):
        raise PimbaError("not number taken")

    def get_text(self):
        return ""

    def __str__(self):
        return ""
Token.EOF = Token(-1)  # to initialize the class variable into its own instance


class NumToken(Token):
    def __init__(self, line_number, value):
        super(NumToken, self).__init__(line_number)
        self.value = value

    def is_number(self):
        return True

    def get_number(self):
        return self.value

    def get_text(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


class StrToken(Token):
    def __init__(self, line_number, value):
        super(StrToken, self).__init__(line_number)
        self.value = value

    def is_string(self):
        return True

    def get_text(self):
        return self.value

    def __str__(self):
        return self.value


class IdToken(Token):
    def __init__(self, line_number, value):
        super(IdToken, self).__init__(line_number)
        self.value = value

    def is_identifier(self):
        return True

    def get_text(self):
        return self.value

    def __str__(self):
        return self.value

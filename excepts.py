#!/usr/bin/python
# -*- coding=utf-8 -*-


# parsing error of Pimba lang
class PimbaParseError(IOError):
    def __init__(self, msg="", token=None):
        if token:
            super(PimbaParseError, self).__init__("invalid Pimba syntax in " + self._location(token) + ". " + msg)
        elif msg:
            super(PimbaParseError, self).__init__(msg)

    @staticmethod
    def _location(token):
        from pimba_token import Token
        if token == Token.EOF:
            return "the last line"
        else:
            return "\"" + token.get_text() + "\" at line " + str(token.get_line_number())


# runtime error of Pimba lang
class PimbaError(RuntimeError):
    def __init__(self, msg, tree=None):
        super(PimbaError, self).__init__(tree and msg + " " + str(tree.location()) or msg)

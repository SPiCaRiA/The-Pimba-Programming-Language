#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTLeaf


class StringLiteral(ASTLeaf):
    def __init__(self, token):
        super(StringLiteral, self).__init__(token)

    def value(self):
        return super(StringLiteral, self).token().get_text()

    def eval(self, env):
        return self.value()

    def __str__(self):
        return super(StringLiteral, self).__str__()

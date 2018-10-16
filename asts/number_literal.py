#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTLeaf


class NumberLiteral(ASTLeaf):
    def __init__(self, token):
        super(NumberLiteral, self).__init__(token)

    def value(self):
        return super(NumberLiteral, self).token().get_number()

    def eval(self, env):
        return self.value()

    def __str__(self):
        return super(NumberLiteral, self).__str__()

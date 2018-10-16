#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList
from excepts import PimbaError


class NegativeExpr(ASTList):
    def __init__(self, children):
        super(NegativeExpr, self).__init__(children)

    def operand(self):
        return super(NegativeExpr, self).child(0)

    def eval(self, env):
        value = self.operand().eval(env)
        if isinstance(value, int):
            return -value
        else:
            raise PimbaError("bad type for -", self)

    def __str__(self):
        return "-" + str(self.operand())

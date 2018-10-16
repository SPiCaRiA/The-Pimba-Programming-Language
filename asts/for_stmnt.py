#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList
from pimba_evaluator import PimbaEvalutaor

TRUE = PimbaEvalutaor.TRUE
FALSE = PimbaEvalutaor.FALSE


class ForStmnt(ASTList):
    def __init__(self, children):
        super(ForStmnt, self).__init__(children)

    def init(self):
        return super(ForStmnt, self).child(0)

    def condition(self):
        return super(ForStmnt, self).child(1)

    def addon(self):
        return super(ForStmnt, self).child(2)

    def body(self):
        return super(ForStmnt, self).child(3)

    def eval(self, env):
        self.init().eval(env)
        result = 0
        while True:
            condition = self.condition().eval(env)
            if isinstance(condition, int) and condition != FALSE:
                result = self.body().eval(env)
                self.addon().eval(env)
            else:
                return result

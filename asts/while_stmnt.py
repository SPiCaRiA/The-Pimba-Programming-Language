#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList
from pimba_evaluator import PimbaEvalutaor

TRUE = PimbaEvalutaor.TRUE
FALSE = PimbaEvalutaor.FALSE


class WhileStmnt(ASTList):
    def __init__(self, children):
        super(WhileStmnt, self).__init__(children)

    def condition(self):
        return super(WhileStmnt, self).child(0)

    def body(self):
        return super(WhileStmnt, self).child(1)

    def eval(self, env):
        while True:
            result = 0
            condition = self.condition().eval(env)
            if isinstance(condition, int) and condition == FALSE:
                return result
            else:
                result = self.body().eval(env)

    def __str__(self):
        return "(while " + str(self.condition()) + " " + str(self.body()) + ")"

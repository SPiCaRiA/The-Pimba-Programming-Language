#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList
from pimba_evaluator import PimbaEvalutaor

TRUE = PimbaEvalutaor.TRUE
FALSE = PimbaEvalutaor.FALSE


class IfStmnt(ASTList):
    def __init__(self, children):
        super(IfStmnt, self).__init__(children)

    def condition(self):
        return super(IfStmnt, self).child(0)

    def then_block(self):
        return super(IfStmnt, self).child(1)

    def else_block(self):
        return super(IfStmnt, self).num_children() > 2 and super(IfStmnt, self).child(2) or None

    def eval(self, env):
        condition = self.condition().eval(env)
        if isinstance(condition, int) and condition != FALSE:
            return self.then_block().eval(env)
        else:
            else_block = self.else_block()
            if not else_block:
                return 0
            else:
                return else_block.eval(env)

    def __str__(self):
        return "(if " + str(self.condition()) + " " + str(self.then_block()) + " else " + str(self.else_block()) + ")"

#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList


class PrimaryExpr(ASTList):
    def __init__(self, children):
        super(PrimaryExpr, self).__init__(children)

    def create(children):
        return len(children) == 1 and children[0] or PrimaryExpr(children)

    def operand(self):
        return super(PrimaryExpr, self).child(0)

    def postfix(self, nest):
        return super(PrimaryExpr, self).child(super(PrimaryExpr, self).num_children() - nest - 1)

    def has_postfix(self, nest):
        return super(PrimaryExpr, self).num_children() - nest > 1

    def eval(self, env):
        return self.eval_sub_expr(env, 0)

    def eval_sub_expr(self, env, nest):
        if self.has_postfix(nest):
            target = self.eval_sub_expr(env, nest + 1)
            return self.postfix(nest).eval(env, target)
        else:
            return self.operand().eval(env)

    def __str__(self):
        return super(PrimaryExpr, self).__str__()

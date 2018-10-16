#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList
from asts.lists.list_ref import ListRef
from asts.name import Name
from asts.primary_expr import PrimaryExpr
from excepts import PimbaError
from pimba_evaluator import PimbaEvalutaor

TRUE = PimbaEvalutaor.TRUE
FALSE = PimbaEvalutaor.FALSE


class BinaryExpr(ASTList):
    def __init__(self, children):
        super(BinaryExpr, self).__init__(children)

    def left(self):
        return super(BinaryExpr, self).child(0)

    def operator(self):
        return super(BinaryExpr, self).child(1).token().get_text()

    def right(self):
        return super(BinaryExpr, self).child(2)

    def eval(self, env):
        operator = self.operator()
        if operator in ["=", "+=", "-="]:
            right = self.right().eval(env)
            return self.compute_assign(env, operator, right)
        else:
            left = self.left().eval(env)
            right = self.right().eval(env)
            return self.compute(left, operator, right)

    def compute_assign(self, env, operator, right):
        left = self.left()
        if isinstance(left, PrimaryExpr):
            if left.has_postfix(0) and isinstance(left.postfix(0), ListRef):
                lst = left.eval_sub_expr(env, 1)
                if isinstance(lst, list):
                    list_ref = left.postfix(0)
                    index = list_ref.index().eval(env)
                    if isinstance(index, int):
                        lst[index] = right
                        return right
        if isinstance(left, Name):
            if operator == "=":
                env[left.name()] = right
                return env[left.name()]
            elif operator == "+=":
                env[left.name()] += right
                return env[left.name()]
            elif operator == "-=":
                env[left.name()] -= right
                return env[left.name()]
        raise PimbaError("bad assignment", self)

    def compute(self, left, operator, right):
        if isinstance(left, int) and isinstance(right, int):
            if operator == "/":
                return left / right
            elif operator == "%":
                return left % right
        if operator == "+":
            return left + right
        elif operator == "-":
            return left - right
        elif operator == "*":
            return left * right
        elif operator == "==":
            return left == right and TRUE or FALSE
        elif operator == ">":
            return left > right and TRUE or FALSE
        elif operator == "<":
            return left < right and TRUE or FALSE
        else:
            raise PimbaError("bad operator", self)

    def __str__(self):
        return super(BinaryExpr, self).__str__()

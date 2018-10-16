#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList
from asts.func.function import Function


class Lambda(ASTList):
    def __init__(self, children):
        super(Lambda, self).__init__(children)

    def parameters(self):
        return super(Lambda, self).child(0)

    def body(self):
        return super(Lambda, self).child(1)

    def eval(self, env):
        return Function(self.parameters(), self.body(), env)

    def __str__(self):
        return "(lambda " + str(self.parameters()) + " " + str(self.body()) + ")"

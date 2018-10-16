#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList
from asts.func.function import Function


class DefStmnt(ASTList):
    def __init__(self, children):
        super(DefStmnt, self).__init__(children)

    def name(self):
        return super(DefStmnt, self).child(0).token().get_text()

    def parameters(self):
        return super(DefStmnt, self).child(1)

    def body(self):
        return super(DefStmnt, self).child(2)

    def eval(self, env):
        env[self.name()] = Function(self.parameters(), self.body(), env)
        return self.name()

    def __str__(self):
        return "(" + self.name() + " " + str(self.parameters()) + " " + str(self.body()) + ")"

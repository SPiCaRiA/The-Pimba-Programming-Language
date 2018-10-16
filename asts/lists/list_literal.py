#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList


class ListLiteral(ASTList):
    def __init__(self, children):
        super(ListLiteral, self).__init__(children)

    def size(self):
        return super(ListLiteral, self).num_children()

    def eval(self, env):
        return [astree.eval(env) for astree in super(ListLiteral, self).children()]

#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList
from asts.null_stmnt import NullStmnt


class BlockStmnt(ASTList):
    def __init__(self, children):
        super(BlockStmnt, self).__init__(children)

    def eval(self, env):
        result = 0
        for tree in super(BlockStmnt, self).children():
            if not isinstance(tree, NullStmnt):
                result = tree.eval(env)
        return result

    def __str__(self):
        return super(BlockStmnt, self).__str__()

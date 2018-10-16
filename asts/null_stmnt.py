#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList


class NullStmnt(ASTList):
    def __init__(self, children):
        super(NullStmnt, self).__init__(children)

    def __str__(self):
        return super(NullStmnt, self).__str__()

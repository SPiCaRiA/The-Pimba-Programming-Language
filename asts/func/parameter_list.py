#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList


class ParameterList(ASTList):
    def __init__(self, children):
        super(ParameterList, self).__init__(children)

    def name(self, index):
        return super(ParameterList, self).child(index).token().get_text()

    def size(self):
        return super(ParameterList, self).num_children()

    def eval(self, env, index, value):
        env[self.name(index)] = value

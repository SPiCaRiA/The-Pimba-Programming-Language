#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.func.arguments import Postfix


class ListRef(Postfix):
    def __init__(self, children):
        super(ListRef, self).__init__(children)

    def index(self):
        return super(ListRef, self).child(0)

    def eval(self, env, value):
        if isinstance(value, list):
            index = self.index().eval(env)
            if isinstance(index, int):
                return value[index]

    def __str__(self):
        return "[" + str(self.index()) + "]"

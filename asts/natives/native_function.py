#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from excepts import PimbaError


class NativeFunction(object):
    def __init__(self, name, method):
        self.name = name
        self.method = method

    def invoke(self, args, tree):
        args = len(args) == 1 and args[0] or args
        try:
            return self.method(args)
        except TypeError:
            raise PimbaError("bad natives function call: " + self.name, tree)

    def __str__(self):
        return "<natives:" + str(id(self)) + ">"

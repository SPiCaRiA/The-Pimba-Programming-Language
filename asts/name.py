#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTLeaf
from excepts import PimbaError


class Name(ASTLeaf):
    def __init__(self, token):
        super(Name, self).__init__(token)

    def name(self):
        return super(Name, self).token().get_text()

    def eval(self, env):
        if not env[self.name()]:
            raise PimbaError("undefined name: " + self.name(), self)
        return env[self.name()]

    def __str__(self):
        return super(Name, self).token().get_text()

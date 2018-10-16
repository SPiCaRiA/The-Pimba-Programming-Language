#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from excepts import PimbaError


class Environment(dict):
    def __init__(self, outer=None):
        self.outer = None
        if not outer:
            super(Environment, self).__init__()
        else:
            self.outer = outer

    def set_outer(self, outer):
        self.outer = outer

    def where(self, name):
        if name in self:
            return self
        elif self.outer:
            return self.outer.where(name)
        else:
            return None

    def __setitem__(self, key, value):
        env = self.where(key)
        if not env:
            super(Environment, self).__setitem__(key, value)
        else:
            super(Environment, env).__setitem__(key, value)

    def __getitem__(self, key):
        if key in self:
            return super(Environment, self).__getitem__(key)
        elif self.outer:
            return self.outer[key]
        return None

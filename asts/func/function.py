#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from environment import Environment


class Function(object):
    def __init__(self, parameter, body, env):
        self.parameter = parameter
        self.body = body
        self.env = env

    def parameters(self):
        return self.parameter

    def body(self):
        return self.body

    def make_env(self):
        return Environment(self.env)

    def __str__(self):
        return "<func:" + str(id(self)) + ">"

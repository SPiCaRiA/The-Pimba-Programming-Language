#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList
from asts.func.function import Function
from asts.natives.native_function import NativeFunction
from excepts import PimbaError


class Postfix(ASTList):
    def __init__(self, children):
        super(Postfix, self).__init__(children)

    def eval(self, env, value):
        raise NotImplementedError("invoking eval() in Postfix object.")


class Arguments(Postfix):
    def __init__(self, children):
        super(Arguments, self).__init__(children)

    def size(self):
        return super(Arguments, self).num_children()

    def eval(self, env, value):
        if not isinstance(value, NativeFunction):
            return self.eval_func(env, value)
        args = []
        for astree in super(Arguments, self).children():
            args.append(astree.eval(env))
        return value.invoke(args, self)

    def eval_func(self, env, value):
        if not isinstance(value, Function):
            raise PimbaError("bad function", self)
        params = value.parameters()
        if self.size() != params.size():
            raise PimbaError("bad number of arguments", self)
        new_env = value.make_env()
        num = 0
        for astree in super(Arguments, self).children():
            params.eval(new_env, num, astree.eval(env))
            num += 1
        return value.body.eval(new_env)

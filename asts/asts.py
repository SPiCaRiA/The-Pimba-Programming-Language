#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from excepts import PimbaError


class ASTree(object):
    def __init__(self):
        raise NotImplementedError("invoking __init__() in ASTree object.")

    def child(self, index):
        raise NotImplementedError("invoking child() in ASTree object.")

    def num_children(self):
        raise NotImplementedError("invoking num_children() in ASTree object.")

    def children(self):
        raise NotImplementedError("invoking children() in ASTree object.")

    def location(self):
        raise NotImplementedError("invoking location() in ASTree object.")

    def eval(self, env):
        raise NotImplementedError("invoking eval() in ASTree object.")


class ASTLeaf(ASTree):
    def __init__(self, token):
        self._token = token
        self.empty_children = []

    def child(self, index):
        raise IndexError("using child() on ASTLeaf object.")

    def num_children(self):
        return 0

    def children(self):
        return self.empty_children

    def location(self):
        return "at line " + str(self._token.get_line_number())

    def token(self):
        return self._token

    def eval(self, env):
        raise PimbaError("cannot eval: " + self.__str__(), self)

    def __str__(self):
        return str(self._token)


class ASTList(ASTree):
    def __init__(self, children):
        self.children = children

    def child(self, index):
        return self.children[index]

    def num_children(self):
        return len(self.children)

    def children(self):
        return self.children

    def location(self):
        for child in self.children:
            child_location = child.location()
            if child_location:
                return self.location
        return None

    def eval(self, env):
        raise PimbaError("cannot eval: " + self.__str__(), self)

    def __str__(self):
        result = "("
        sep = ""
        for child in self.children:
            result += sep
            sep = " "
            result += str(child)
        result += ")"
        return result


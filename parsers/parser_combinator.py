#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.asts import ASTList
from asts.asts import ASTLeaf
from excepts import PimbaParseError


class Element(object):
    def __init__(self):
        raise NotImplementedError("invoking constructor in Element object.")

    def parse(self, lexer, result):
        raise NotImplementedError("invoking parse() in Element object.")

    def match(self, lexer):
        raise NotImplementedError("invoking match() in Element object.")


class Tree(Element):
    def __init__(self, parser):
        self.parser = parser

    def parse(self, lexer, result):
        result.append(self.parser.parse(lexer))

    def match(self, lexer):
        return self.parser.match(lexer)


class OrTree(Element):
    def __init__(self, parsers):
        self.parsers = parsers

    def parse(self, lexer, result):
        parser = self.choose(lexer)
        if parser:
            result.append(parser.parse(lexer))
        else:
            raise PimbaParseError(lexer.peek(0))

    def match(self, lexer):
        return bool(self.choose(lexer))

    def choose(self, lexer):
        for parser in self.parsers:
            if parser.match(lexer):
                return parser
        return None

    def insert(self, parser):
        self.parsers = [parser] + list(self.parsers)


class Repeat(Element):
    def __init__(self, parser, once):
        self.parser = parser
        self.once = once

    def parse(self, lexer, result):
        while self.parser.match(lexer):
            tree = self.parser.parse(lexer)
            if not (ASTList == tree.__class__) or tree.num_children() > 0:
                result.append(tree)
            if self.once:
                break

    def match(self, lexer):
        return self.parser.match(lexer)


class AToken(Element):
    def __init__(self, token_type):
        self.token_type = token_type
        if not token_type:
            self.token_type = ASTLeaf
        self.factory = Factory.get(self.token_type)

    def parse(self, lexer, result):
        token = lexer.read()
        if self.test(token):
            leaf = self.factory.make(token)
            result.append(leaf)
        else:
            raise PimbaParseError(token)

    def match(self, lexer):
        return self.test(lexer.peek(0))

    def test(self, token):
        raise NotImplementedError("invoking test() in AToken object.")


class IdToken(AToken):
    def __init__(self, token_type, reserved):
        super(IdToken, self).__init__(token_type)
        self.reserved = reserved and reserved or []

    def test(self, token):
        return token.is_identifier() and not (token.get_text() in self.reserved)


class NumToken(AToken):
    def __init__(self, token_type):
        super(NumToken, self).__init__(token_type)

    def test(self, token):
        return token.is_number()


class StrToken(AToken):
    def __init__(self, token_type):
        super(StrToken, self).__init__(token_type)

    def test(self, token):
        return token.is_string()


class Leaf(Element):
    def __init__(self, token_pats):
        self.token_pats = token_pats

    def parse(self, lexer, result):
        token = lexer.read()
        if token.is_identifier():
            for token_pat in self.token_pats:
                if token_pat == token.get_text():
                    self.find(result, token)
                    return
        if len(self.token_pats) > 0:
            raise PimbaParseError(self.token_pats[0] + " expected.", token)
        else:
            raise PimbaParseError(token)

    def find(self, result, token):
        result.append(ASTLeaf(token))

    def match(self, lexer):
        token = lexer.peek(0)
        if token.is_identifier():
            for token_pat in self.token_pats:
                if token_pat == token.get_text():
                    return True
        return False


class Skip(Leaf):
    def __init__(self, token_pats):
        super(Skip, self).__init__(token_pats)

    def find(self, result, token):
        pass  # skip the token when found


# operator precedence parsing
class Precedence(object):
    def __init__(self, value, left_associative):
        self.value = value
        self.left_associative = left_associative


class Operators(dict):
    RIGHT = False
    LEFT = True

    def add(self, name, precedence, left_associative):
        self[name] = Precedence(precedence, left_associative)


class Expr(Element):
    def __init__(self, clazz, expression, operators):
        self.factory = Factory.get_for_astlist(clazz)
        self.operators = operators
        self.factor = expression

    def parse(self, lexer, result):
        right = self.factor.parse(lexer)

        precedence = self.next_operator(lexer)
        while precedence:
            right = self.do_shift(lexer, right, precedence.value)
            precedence = self.next_operator(lexer)
        result.append(right)

    def next_operator(self, lexer):
        token = lexer.peek(0)
        if token.is_identifier():
            return token.get_text() in self.operators and self.operators[token.get_text()] or None
        else:
            return None

    def do_shift(self, lexer, left, precedence):
        make_list = [left, ASTLeaf(lexer.read())]
        right = self.factor.parse(lexer)

        next_op = self.next_operator(lexer)
        while next_op and self.right_is_expr(precedence, next_op):
            right = self.do_shift(lexer, right, next_op.value)
            next_op = self.next_operator(lexer)
        make_list.append(right)
        return self.factory.make(make_list)

    @staticmethod
    def right_is_expr(precedence, next_precedence):
        if next_precedence.left_associative:
            return precedence < next_precedence.value
        else:
            return precedence <= next_precedence.value

    def match(self, lexer):
        return self.factor.match(lexer)


class Factory(object):
    factory_name = "create"  # name of create method of PrimaryExpr

    def make0(self, args):  # implemented when producing the factory instance through get()/get_for_ASTList()
        raise NotImplementedError("invoking make0 in Factory object")

    def make(self, args):
        try:
            return self.make0(args)
        except TypeError:
            raise

    @staticmethod
    def get_for_astlist(clazz):
        factory = Factory.get(clazz)
        if not factory:
            factory = Factory()
            factory.make0 = lambda args: len(args) == 1 and args[0] or ASTList(args)
        return factory

    @staticmethod
    def get(clazz):
        if not clazz:
            return None
        if Factory.factory_name in dir(clazz):
            factory = Factory()
            factory.make0 = lambda args: clazz.__dict__[Factory.factory_name](args)
        else:
            factory = Factory()
            factory.make0 = lambda args: clazz(args)
        return factory


class Parser(object):
    def __init__(self, parser_or_clazz):
        self.elements = None
        self.factory = None
        if isinstance(parser_or_clazz, Parser):  # if is parser
            self.elements = parser_or_clazz.elements
            self.factory = parser_or_clazz.factory
        else:
            self.reset(clazz=parser_or_clazz)

    def parse(self, lexer):
        results = []
        for element in self.elements:
            element.parse(lexer, results)
        return self.factory.make(results)

    def match(self, lexer):
        if len(self.elements) == 0:
            return True
        else:
            element = self.elements[0]
            return element.match(lexer)

    # static DSL methods
    @staticmethod
    def rule(clazz=None):
        return Parser(clazz)

    def reset(self, **kwargs):
        self.elements = []
        if "clazz" in kwargs:  # ??
            clazz = kwargs["clazz"]
            self.factory = Factory.get_for_astlist(clazz)
        return self

    def number(self, clazz=None):
        self.elements.append(NumToken(clazz))
        return self

    # *
    def identifier(self, reserved, clazz=None):
        self.elements.append(IdToken(clazz, reserved))
        return self

    def string(self, clazz=None):
        self.elements.append(StrToken(clazz))
        return self

    def token(self, *token_pats):
        self.elements.append(Leaf(token_pats))
        return self

    def sep(self, *token_pats):
        self.elements.append(Skip(token_pats))
        return self

    def ast(self, parser):
        self.elements.append(Tree(parser))
        return self

    def oor(self, *parsers):
        self.elements.append(OrTree(parsers))
        return self

    def maybe(self, parser):
        root = Parser(parser)
        root.reset()
        self.elements.append(OrTree([parser, root]))
        return self

    def option(self, parser):
        self.elements.append(Repeat(parser, True))
        return self

    def repeat(self, parser):
        self.elements.append(Repeat(parser, False))
        return self

    # *
    def expression(self, sub_expr, operators, clazz=None):
        self.elements.append(Expr(clazz, sub_expr, operators))
        return self

    def insert_choice(self, parser):
        element = self.elements[0]
        if isinstance(element, OrTree):
            element.insert(parser)
        else:
            otherwise_parser = Parser(self)
            self.reset(clazz=None)
            self.oor(parser, otherwise_parser)
        return self


# encapsulation of Parser.rule()
# can be directly imported by other modules
def rule(clazz=None):
    return Parser.rule(clazz)

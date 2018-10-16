#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from asts.binary_expr import BinaryExpr
from asts.block_stmnt import BlockStmnt
from asts.for_stmnt import ForStmnt
from asts.func.arguments import Arguments
from asts.func.def_stmnt import DefStmnt
from asts.func.parameter_list import ParameterList
from asts.func.lambda_func import Lambda
from asts.if_stmnt import IfStmnt
from asts.lists.list_literal import ListLiteral
from asts.lists.list_ref import ListRef
from asts.negative_expr import NegativeExpr
from asts.name import Name
from asts.null_stmnt import NullStmnt
from asts.number_literal import NumberLiteral
from asts.primary_expr import PrimaryExpr
from asts.string_literal import StringLiteral
from asts.while_stmnt import WhileStmnt
from parsers.parser_combinator import rule
from parsers.parser_combinator import Operators
from pimba_token import Token


class PimbaParser(object):
    def __init__(self):
        self.reserved = []
        self.reserved.append(";")
        self.reserved.append("}")
        self.reserved.append(")")
        self.reserved.append("]")
        self.reserved.append(Token.EOL)
        operators = Operators()
        operators.add("=", 1, Operators.RIGHT)
        operators.add("+=", 1, Operators.RIGHT)
        operators.add("-=", 1, Operators.RIGHT)
        operators.add("==", 2, Operators.LEFT)
        operators.add(">", 2, Operators.LEFT)
        operators.add("<", 2, Operators.LEFT)
        operators.add("+", 3, Operators.LEFT)
        operators.add("-", 3, Operators.LEFT)
        operators.add("*", 4, Operators.LEFT)
        operators.add("/", 4, Operators.LEFT)
        operators.add("%", 4, Operators.LEFT)

        expr0 = rule()
        #  primary:      "(" expr ")" | NUMBER | IDENTIFIER | STRING
        primary = rule(PrimaryExpr).oor(rule().sep("(").ast(expr0).sep(")"),
                                        rule().number(NumberLiteral),
                                        rule().identifier(self.reserved, Name),
                                        rule().string(StringLiteral))

        #  factor:       "-" primary | primary
        factor = rule().oor(rule(NegativeExpr).sep("-").ast(primary), primary)

        #  expr:         factor { OP factor }
        expr = expr0.expression(factor, operators, BinaryExpr)

        statement0 = rule()
        #  block:        "{" [ statement ] {(";" | EOL) [ statement ]} "}"
        block = rule(BlockStmnt).sep("{").option(statement0).repeat(rule().sep(";", Token.EOL).option(statement0)).sep(
            "}")

        #  simple:       expr
        simple = rule(PrimaryExpr).ast(expr)

        #  statement:  "if" expr block [ "else" block ] | "while" expr block | "for (" expr expr expr ")" block | simple
        statement = statement0.oor(rule(IfStmnt).sep("if").ast(expr).ast(block).option(rule().sep("else").ast(block)),
                                   rule(WhileStmnt).sep("while").ast(expr).ast(block),
                                   rule(ForStmnt).sep("for").sep("(").ast(expr).sep(";").ast(expr).sep(";").ast(expr).
                                   sep(")").ast(block),
                                   simple)

        # function
        # param:        IDENTIFIER
        param = rule().identifier(self.reserved)

        # params:       param { "," param }
        params = rule(ParameterList).ast(param).repeat(rule().sep(",").ast(param))

        # param_list:   "(" [ params ] ")
        param_list = rule().sep("(").maybe(params).sep(")")

        # def:          "def" IDENTIFIER param_list block
        define = rule(DefStmnt).sep("def").identifier(self.reserved).ast(param_list).ast(block)

        # args:         expr { "," expr }
        args = rule(Arguments).ast(expr).repeat(rule().sep(",").ast(expr))

        # postfix:      "(" [ args ] ")"
        postfix = rule().sep("(").maybe(args).sep(")")

        # primary:      "lambda" param_list block | ( "(" expr ")" | NUMBER | IDENTIFIER | STRING ) { postfix }
        primary.repeat(postfix).insert_choice(rule(Lambda).sep("lambda").ast(param_list).ast(block))

        # simple:       expr [ args ]
        simple.option(args)

        # list
        # elements:     expr { "," expr }
        elements = rule(ListLiteral).ast(expr).repeat(rule().sep(",").ast(expr))

        # primary:      ( "[" [ elements ] "]" | "(" expr ")" | NUMBER | IDENTIFIER | STRING ) { postfix }
        primary.insert_choice(rule().sep("[").maybe(elements).sep("]"))

        # postfix:      "(" [ args ] ")"  | "[" expr "]"
        postfix.insert_choice(rule(ListRef).sep("[").ast(expr).sep("]"))

        #  program:      [ define | statement ] (";" | EOL)
        self.program = rule().oor(statement, rule(NullStmnt)).sep(";", Token.EOL).insert_choice(define)

    def parse(self, lexer):
        return self.program.parse(lexer)

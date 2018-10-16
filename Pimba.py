#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
import argparse
import os.path
import time

from excepts import PimbaError
from interpreters.pimba_interpreter import PimbaInterpreter
from interpreters.repl import REPL


class Pimba(object):
    def __init__(self, args):
        self.args = args
        self.interpreter = None

    def run(self):
        if not self.args.filename:
            self.run_repl()
        else:
            self.run_file(self.args.filename)

    def run_repl(self):
        print "Type in expression to have them evaluated.\n"
        while True:
            try:
                line = raw_input(">>> ")
                while not line:
                    line = raw_input(">>> ")
                while line.count("{") > line.count("}") or \
                      line.count("(") > line.count(")"):
                    line += "\n" + raw_input("... ")
                self.interpret_repl(line)
            except KeyboardInterrupt:
                print "\nKeyboardInterrupt"

    def interpret_repl(self, characters):
        self.interpreter = self.interpreter and self.interpreter or REPL()
        self.interpreter(characters)

    def run_file(self, filename):
        filename = os.path.expanduser(filename).replace("\\", "/")
        if filename[-2:] != "sc":
            raise IOError("not Pimba script file!")
        try:
            script = open(filename, "r")
        except IOError:
            raise PimbaError("No such file or directory: \'%s\'" % filename)
        self.interpret(script.readlines())

    def interpret(self, characters):
        self.interpreter = PimbaInterpreter(characters)
        self.interpreter()

    def __call__(self):
        self.run()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename", nargs="?", default="", help="script file the program read from")
    args = argparser.parse_args()
    Pimba(args)()

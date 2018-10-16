#!/usr/bin/python
# -*- coding=utf-8 -*-

from interpreters.pimba_interpreter import PimbaInterpreter


def interpreter_test(characters):
    PimbaInterpreter(characters).test()

if __name__ == "__main__":
    test_characters = """i = 1
while i < 10 {
    println(i)
    i = i + 1
}"""
    interpreter_test(test_characters)


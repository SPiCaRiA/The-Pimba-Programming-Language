#!/usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from asts.natives.native_function import NativeFunction
from excepts import PimbaError


class Natives(object):
    def __init__(self, interpreter):
        self.env = None
        self.interpreter = interpreter

        # Natives
        self.native_func = {
            # Basic IO
            "print": lambda args: print(args, end="") and 0 or None,
            "println": lambda args: print(args) and 0 or None,
            "input": lambda prompt: raw_input(prompt),

            # Basic buildins
            "eval": self.run,
            "import": lambda module_name: self._import(module_name),
            "dir": self.dir,
            "int": lambda value: self.to_int,

            # Basic calculations
            "len": len,
            "sum": lambda lst: sum(lst),

            # Easter eggs
            "milk": lambda arg: arg == "poison" and poison_milk or
                               (arg == "maru" and "Maru打得真是好" or
                               (arg == "life" and "Life就是一只鸡")),
        }

        # Buildins
        self.string = {
            "upper": lambda string: string.upper(),
            "lower": lambda string: string.lower(),
            "isdigit": lambda string: string.isdigit(),
            "strip": lambda string: string.strip(),
        }
        self.lisp = {
            "cdr": lambda lst: lst and lst[1:] or lst,
            "car": lambda lst: lst[0],
            "cons": lambda args: (isinstance(args[0], list) and args[0] or [args[0]]) +
                                 (isinstance(args[1], list) and args[1] or [args[1]]),
            "max": lambda lst: max(lst),
            "min": lambda lst: min(lst),
        }
        self.file = {
            "read": self.read_file,
        }
        self.build_ins = {
            "this": None,
            "string": self.string,
            "lisp": self.lisp,
            "file": self.file,
        }

    def environment(self, env):
        self.append_natives(env)
        self.env = env
        return env

    def append_natives(self, env):
        for method in self.native_func:
            self.append(env, method)

    def append(self, env, method_name):
        env[method_name] = NativeFunction(method_name, self.native_func[method_name])

    def run(self, string):
        self.interpreter(string)

    def _import(self, module_name):
        if module_name in self.build_ins:
            return self.import_buildins(module_name)
        else:
            self.run(self.read_file(module_name))

    def import_buildins(self, module_name):
        if module_name == "this":
            return zen_of_sc
        else:
            self.native_func.update(self.build_ins[module_name])
            for method in self.build_ins[module_name]:
                self.append(self.env, method)

    def dir(self, module_name):
        if not module_name:
            return self.env.keys()
        else:
            if module_name in self.build_ins:
                if module_name == "this":
                    return ["'zen_of_sc'"]
                return self.build_ins[module_name].keys()
            else:
                raise PimbaError("dir() cannot show namespace of customized modules.")

    @staticmethod
    def to_int(value):
        if isinstance(value, str) or isinstance(value, int):
            return int(value)
        else:
            raise PimbaError(str(value))

    @staticmethod
    def read_file(filename):
        with open(filename, "r") as _file:
            return _file.read()

    @staticmethod
    def write_file(filename, string):
        with open(filename, "w") as _file:
            _file.write(string)


poison_milk = "飞龙骑脸 小明打得菜\n妈妈船回头 亲本出问题\n两个巨像jim都a不死人\n" + \
              "烦死了和我有什么关系\n我的专业解说 一句话一百人口差距\nMaru打得好，Life就是鸡\n我解说不来了这个游戏\n" + \
              "Snute也证明了自己是非韩第一人\n但是无奈 他面对的是God 是神\n是史上最强的星际二选手\n" + \
              "错了 是史上最强的星际选手\n吔 哎呀 我对不起你啊教主\n"

zen_of_sc = "How to Play Starcraft: \n" + \
            "狗偷稳谐莽奶\n" + \
            "狗克偷 偷克稳 稳克谐 谐克莽 莽克狗 奶克万物\n" + \
            "Z:\nZVT: 12D毒爆一波\nZVZ: 裸三狗毒爆or12D插管子一波\nZVP: 诸神的黄昏\n\n" + \
            "T:\nTVZ: 醉梦罗汉拳\nTVT: 鸡谐化转城市化\nTVP: 野3BB\n\n" + \
            "P:\nPVZ: 诛仙剑阵\nPVT: 6bg使徒克一切\nPVP: 闪追多线送兵跳自爆球\n"

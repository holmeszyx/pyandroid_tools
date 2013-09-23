#!/usr/bin/env python
# -*- coding: UTF-8 -*-

try:
    import sys
    from os import popen3 as pipe
except ImportError, e:
    print("require mode no found")
    exit(-1)

class AAPT():
    __aapt_path = None
    __output = None
    __error = None

    def __init__(self, aapt_path = None):
        self.__aapt_path = aapt_path

    def __clean__(self):
        self.__output = None
        self.__error = None

    def __read_output__(self,fd):
        ret = ''
        while True:
            line = fd.readline()
            if not line:
                break
            ret += line

        if len(ret) == 0:
            ret = None

        return ret

    def __run_commond__(self, cmd):
        self.__clean__()
        try:
            w, r, e = pipe(self.__build_commond__(cmd), mode = "r")
            self.__output = self.__read_output__(r)
            self.__error = self.__read_output__(e)
            w.close()
            r.close()
            e.close()
        except Exception, exce:
            print(exce)
            print("run commd error")

    def __build_commond__(self, cmd):
        return self.__aapt_path + " " + cmd

    def set_aapt_path(self, path):
        self.__aapt_path = path

    def __build_dump_cmd__(self, cmd):
        return "d " + cmd

    def dump_badging(self, apk):
        self.__run_commond__("d badging " + apk)
        return self.__output

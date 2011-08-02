#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2011 Yann GUIBET <yannguibet@gmail.com>
#  See LICENSE for details.

import os, sys
import string
from getpass import getpass

class _getpwd(object):
    base = string.digits+string.letters+string.punctuation
    def __init__(self):
        self.table = [None]*len(self.base)
        for i in self.base:
            while True:
                y = ord(os.urandom(1))%len(self.table)
                if self.table[y] is None:
                    self.table[y] = i
                    break

    def show(self):
        y = 1
        sys.stdout.write("__  _A_|_B_|_C_|_D_|_E_|_F_|_G_|_H_|_I_|_J_|_K_|_L_|_M_|_N_|_O_|_P_")
        for i in range(len(self.table)):
            if i%16 == 0:
                sys.stdout.write("|\n%d |"%y)
                y += 1
            sys.stdout.write("| \033[31m"+self.table[i]+"\033[00m ")
        sys.stdout.write("|\n")

    def get(self, inp):
        inp = getpass(inp)
        if len(inp) % 2 != 0:
            raise Exception, "Error"
        pwd = ""
        for i in range(0, len(inp), 2):
            if inp[i] < 'A' or inp[i] > 'P' or inp[i+1] < '1' or inp[i+1] > '6':
                raise Exception, "Error"
            if inp[i+1] == '6' and inp[i] > 'O':
                raise Exception, "Error"
            pwd += self.table[ord(inp[i])-65+(int(inp[i+1])-1)*16]
        return pwd

def getpwd(inp):
    a = _getpwd()
    a.show()
    return a.get(inp)
    
if __name__ == '__main__':
    print getpwd('Password : ')

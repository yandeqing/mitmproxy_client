#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/4/19 17:05
'''
import os


def exe_shell(shell):
    print(f"【exec_shell().shell={shell}】")
    linesStr = list(os.popen(shell).readlines())
    for line in linesStr:
        print(f"{line}")
def exe_shell_whitout(shell):
    print(f"【exec_shell().shell={shell}】")
    os.system(shell)
#!/usr/bin/env python
import sys

from dict_ti import dict_ti
from dict_me import dict_me

def rep(s, a, b):
        t = s
        t = t.replace(a + ' ', b + ' ')
        t = t.replace(a + ',', b + ',')
        t = t.replace(a + '.', b + '.')
        t = t.replace(a + '!', b + '!')
        t = t.replace(a + '?', b + '?')
        return t


def ti(str):
    t = str
    for key in dict_ti:
        t = rep(t, key, dict_ti[key])
    return t

def me(str):
    t = str
    for key in dict_me:
        t = rep(t, key, dict_me[key])
    return t





def convert(input_file, output_file):
    lines_ti = []
    lines_me = []

    with open(input_file) as FileObj:
        for text in FileObj:
            lines_ti.append(ti(text))
            lines_me.append(me(text))

    with open("ti_" + output_file, 'w', encoding='utf-8') as file:
        file.writelines(lines_ti)

    with open("me_" + output_file, 'w', encoding='utf-8') as file:
        file.writelines(lines_me)



if __name__=='__main__':
    if (len(sys.argv) != 3):
        exit('Usage: make_time.py src_file dest_file')
    convert(sys.argv[1], sys.argv[2])

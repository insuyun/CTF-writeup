from pwn import *
from Crypto.Util.number import *
from gmpy import *
from random import *
import sys,os

NQ = 0

def calcA(r, m):
    global NQ
    NQ += 1
    r.recvuntil('cmd: ')
    r.sendline("A")
    r.recvuntil('input: ')
    r.sendline(long_to_bytes(m).encode('hex'))
    return bytes_to_long(r.readline().strip().decode('hex'))

def calcB(r, m):
    global NQ
    NQ += 1
    r.recvuntil('cmd: ')
    r.sendline("B")
    r.recvuntil('input: ')
    r.sendline(long_to_bytes(m).encode('hex'))
    return bytes_to_long(r.readline().strip().decode('hex'))

def fixup(r, n):
    dec = calcB(r, calcA(r, n | 0xff))
    for i in xrange(256):
        possible_n = n | i
        if (n | 0xff) % possible_n == dec:
            return possible_n
    raise

gmod = 2 ** 8
pt = 0xa

while True:
    NQ = 0
    r = process(['python', 'crypto-33dee9470e5b5639777f7c50e4c650e3.py'])
    #r = remote('13.112.92.9', 21701)
    try:
        r.recvline()
        enc_flag = bytes_to_long(r.recvline().strip().decode('hex'))

        c = calcB(r, calcA(r, 1 << 1023))
        if c == 0:
            n = (1 << 1023)
            bits = 1022
        else:
            n = (1 << 1022)
            bits = 1021

        for i in xrange(bits, 7, -1):
            guess = n | (1 << i)
            if calcB(r, calcA(r, guess)) == 0:
                n = guess

        n = fixup(r, n)

        while NQ < 2048:
            e = (enc_flag * (-pt * n + 1)) % (n*n)
            test = pow(e, invert(gmod, n), n*n)
            d = calcB(r, test)
            pt += d * gmod
            gmod = gmod * (2 ** 8)
            print(long_to_bytes(pt))
            #raw_input()
    finally:
        r.close()

r.interactive()

from pwn import *
from Crypto.Util.number import *
from gmpy import *
import os,sys

NQ = 0

def enc(r, n):
    global NQ
    NQ += 1
    r.recvuntil('cmd: ')
    r.sendline('A')
    r.recvuntil('input: ')
    r.sendline(long_to_bytes(n).encode('hex'))
    return bytes_to_long(r.readline().strip().decode('hex'))

def dec(r, n):
    global NQ
    NQ += 1
    r.recvuntil('cmd: ')
    r.sendline('B')
    r.recvuntil('input: ')
    r.sendline(long_to_bytes(n).encode('hex'))
    return bytes_to_long(r.readline().strip().decode('hex'))

r = process(['python', 'rsa-b667a9ca0d5c6735e5609565d1fd6ab9.py'])
r.readline()
enc_flag = bytes_to_long(r.readline().strip().decode('hex'))

# compute n
m = 2
e = enc(r, m)
n = 0

for i in xrange(16):
    e2 = enc(r, m ** 2)
    n = gcd(e**2 - e2, n)
    e = e2
    m = m ** 2

# leak byte per byte
pt = dec(r, enc_flag)
mod = 1
e = enc_flag

for i in xrange(60):
    mod *= 2 ** 8
    i28 = invert(mod, n)
    e28 = enc(r, i28)

    e = enc_flag * e28
    d = dec(r, e)
    byte = (d - ((pt * i28) % n)) % 256
    pt |= (byte << (8 * i + 8))
    print('ans: %s' % long_to_bytes(pt))

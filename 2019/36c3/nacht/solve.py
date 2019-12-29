#!/usr/bin/env python3
import os, ctypes
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse

lib = ctypes.CDLL('./tweetnacl.so')

def mac(key, msg):
    tag = ctypes.create_string_buffer(16)
    lib.crypto_onetimeauth_poly1305_tweet(tag, key, len(msg), msg)
    return bytes(tag)

def chk(key, tag, msg):
    return not lib.crypto_onetimeauth_poly1305_tweet_verify(tag, key, len(msg), msg)

def le_bytes_to_num(s):
    return bytes_to_long(s[::-1])

def num_to_16_le_bytes(n):
    return long_to_bytes(n)[::-1]

p = (1 << 130) - 5

from pwn import *

r = remote('88.198.156.141', 2833)
#r = process("python3", "-u", "./vuln.py")
messages = []
for i in range(32):
    x, y = r.readline().split()
    messages.append((bytes.fromhex(x.decode()), bytes.fromhex(y.decode())))

for i in range(0, 32):
    for j in range(i + 1, 32):
        k1, t1 = messages[i]
        r1, s1 = le_bytes_to_num(k1[:16]), le_bytes_to_num(k1[16:])
        r1 &= 0x0ffffffc0ffffffc0ffffffc0fffffff
        t1 = le_bytes_to_num(t1)

        k2, t2 = messages[j]
        r2, s2 = le_bytes_to_num(k2[:16]), le_bytes_to_num(k2[16:])
        r2 &= 0x0ffffffc0ffffffc0ffffffc0fffffff
        t2 = le_bytes_to_num(t2)

        m1 = ((t1 - s1) * r2 - (t2 - s2) * r1) * inverse(r2 * r1 * r1 - r2 * r2 * r1, p)
        m2 = ((t1 - s1) * r2 * r2 - (t2 - s2) * r1 * r1) * inverse(r1 * r2 * r2 - r2 * r1 * r1, p)
        m1 %= p
        m2 %= p

        lsb1 = (m1 & (0xff << 128)) >> 128
        lsb2 = (m2 & (0xff << 128)) >> 128
        if lsb1 == 1 and lsb2 == 1:
            m1 -= (1 << 128)
            m2 -= (1 << 128)
            key = num_to_16_le_bytes(m1) + num_to_16_le_bytes(m2)
            break

x, y = r.readline().split()
print(key)
msg = bytes.fromhex(x.decode())
r.write(mac(key, msg).hex() + "\n")
print(r.readline())
# hxp{Oo0o0oO0oo0ps_5t1lL_uPf0cK4bL3}

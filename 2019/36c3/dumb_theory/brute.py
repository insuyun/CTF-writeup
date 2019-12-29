#!/usr/bin/env python3
import random, struct, re, sys, hashlib, random
import uuid
import string
from itertools import permutations

target = 'Hello hxp! I would like the flag, please. Thank you.'
sig = "194569243600128472648342062015620900945718581078353494173333401884054850875530382148788323494132802992884273082200320646651180352429907523311545856531272571557995231739584447242824136038315350789722394381806616996555843201523819424099077350366566358575422722891407165|314349122978694434728684551561785469671849651010192101852953772287589557164109198450542386488424813283093163293376716415751164644227670469718686163362061243159503308486098499593894485545338601338971836042612377812338158418346018686347280572903202583733835245827431772|658809427923956640086186443976234062250773752182448289480474291104895707005936993494036371238492142720002302358792427690877581902347063117281943450254452527933934095614085703137066436116219390382878503503393010711111950989780697508858596625399707429535328743518976972"

import uuid
prefix = str(uuid.uuid4())

print("PREFIX: %s" % prefix)
r = 3
def H(msg):
    h = hashlib.sha256(msg.encode()).digest()
    v = tuple(c+1 for c in struct.unpack(f'>{r}H', h[:r+r]))
    return v

def gen_msg():
    for x in range(0x110000):
        # check if x is fine
        try:
            msg = 'Hello hxp! I would like the flag, please%c Thank you.' % (x)
            data = '%s Signature: %s' % (msg, sig)
            m = re.match(f'({target}) Signature: ([0-9|]+)', data)
            if not m:
                continue
        except UnicodeEncodeError:
            continue

        for y in range(0x110000):
            try:
                msg = 'Hello hxp! I would like the flag, please%c Thank you%c' % (x, y)
                data = '%s Signature: %s' % (msg, sig)
                m = re.match(f'({target}) Signature: ([0-9|]+)', data)
                if m:
                    yield msg, x, y, H(msg)
            except UnicodeEncodeError:
                continue

def scalar_mul(k, t):
    return tuple([x * k for x in t])

def gen_random():
    v = []
    for p in permutations(string.ascii_letters + string.digits, 8):
        s = prefix + ''.join(p)
        yield s, H(s)

map_rand = {}
map_msg = {}
for rand, msg in zip(gen_random(), gen_msg()):
    rand_str, rand_hash = rand
    msg_str, x, y, msg_hash = msg

    if max(rand_hash) < (65536 / 2):
        d = scalar_mul(2, rand_hash)
        if d in map_rand:
            print("[+] Found rand-rand pair")
            print("s1: %s, h1: %s" % (rand_str, H(rand_str)))
            s2 = map_rand[d]
            print("s2: %s, h2: %s" % (s2, H(s2)))

        if d in map_msg:
            print("[+] Found rand-msg pair")
            print("s1: %s, h1: %s" % (rand_str, H(rand_str)))
            s2, c1, c2 = map_msg[d]
            print("msg: %s, c1: %d, c2: %d, h2: %s" % (s2, c1, c2, H(s2)))

    map_rand[rand_hash] = rand_str

    if max(msg_hash) < (65536 / 2):
        d = scalar_mul(2, rand_hash)
        if d in map_rand:
            print("[+] Found rand-msg pair")
            print("msg: %s, c1: %d, c2: %d, h2: %s" % (msg_str, x, y, H(msg_str)))
            s1 = map_rand[d]
            print("s1: %s, h1: %s" % (s1, H(s1)))

    map_msg[msg_hash] = (msg_str, x, y)

    if (len(map_msg) % 0x100000) == 0:
        print("[+] Tick: %s" % len(map_msg))

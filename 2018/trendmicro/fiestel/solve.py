import copy
import os

def xor(l, r):
    return (l | r) - (l & r)

p = '010000010110111000100000011000010111000001110000011011000110010100100000011000010110111001100100001000000110000101101110001000000110111101110010011000010110111001100111011001010010000001110111011001010110111001110100001000000111010001101111001000000101010001110010011001010110111001100100'

c = '000100100011000101110101001101100110001100110001001110100011110101100000011110010010111000110011001110000000110100100101011111000011000000100001010000100110011100100001011000000111001101110100011011100110000000100000011011010110001001100100001011010110111001100110001010110110110101110001'

cipher = '000000110000111001011100001000000001100100101100000100100111111000001001000001100000001100001001000100100010011101001010011000010111100100100010010101110100010001000010010101010100010101111111010001000110000001101001011111110111100001100101011000010010001001001011011000100111001001101011'

n = 144

def cmsg(m):
    c = 0
    if "m0" in m:
        c += 1
    if "m1" in m:
        c += 1
    return c

def bin2int(x):
    return int(x[:n], 2), int(x[n:], 2)

def find_one_pt(ml, mr):
    cl = cmsg(ml)
    cr = cmsg(mr)

    if cl == 1:
        return True
    else:
        assert(cr == 1)
        return False

def int2str(i):
    h = hex(int(''.join([bin(k)[2:].rjust(n, '0') for k in i]), 2))
    if h[-1] == 'L':
        h = h[:-1]
    h = h[2:]
    if len(h) % 2 == 1:
        h = "0" + h
    return h.decode("hex")

def str2bin(s):
    return bin(int(s.encode("hex"), 16))[2:].rjust(2 * n, '0')

def encrypt(ms1, ms2, round=16):
    keys = []
    for i in xrange(round):
        keys.append(int(os.urandom(n / 8).encode("hex"), 16))

    # encrypt ms1
    for i in xrange(round):
        ts = [copy.copy(ms1[0]), copy.copy(ms1[1])]
        ms1 = [ts[1], ts[0] ^ ts[1] ^ keys[i]]

    # encrypt ms2
    for i in xrange(round):
        ts = [copy.copy(ms2[0]), copy.copy(ms2[1])]
        ms2 = [ts[1], ts[0] ^ ts[1] ^ keys[i]]

    return ms1, ms2

# ps = bin2int(p)
# print(int2str(ps))
# 
# p = str2bin("A"*36)
# k = str2bin("B"*36)
# 
# ks = bin2int(k)
# ps = bin2int(p)
# 
# cs, es = encrypt(ps, ks, 1)

ps = bin2int(p)
cs = bin2int(c)
es = bin2int(cipher)

s = set()
for i in xrange(8):
    ms = [{'m0'}, {'m1'}]

    for j in xrange(i):
        ts = [copy.copy(ms[0]), copy.copy(ms[1])]
        ms = [ts[1], xor(ts[0], xor(ts[1], {"k%d" % j}))]

    ks = [None, None]
    used1 = used2 = None

    for j in xrange(2):

        # count the number of mx
        count = 0

        for k in xrange(2):
            if "m%d" % k in ms[j]:
                count += 1
                solo = k

        if count == 1:
            # we can recover this...
            ks[solo] = ps[solo] ^ cs[j] ^ es[j]
            used1 = solo
            used2 = j
    print(ks, ms)
    for j in xrange(2):
        if ks[j] == None:
            print(j, 1-used2)
            ks[j] = ks[1-j] ^ ps[j] ^ ps[1-j]^ cs[1-used2] ^ es[1-used2]

    print(repr(int2str(ks)))

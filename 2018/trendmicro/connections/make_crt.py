import os

certs = [open('certs/%d.crt' % i, 'rb').read() for i in xrange(1, 13)]

if not os.path.exists('certs'):
    os.mkdir('certs')

ns = []
for i,cert in enumerate(certs):
    with open("certs/cert%d.der" % i, "wb") as f:
        f.write(cert)
    os.system("openssl x509 -inform der -in {0}.der -out {0}.pem".format("certs/cert%d" % i))
    os.system("openssl x509 -inform pem -in {0}.pem -pubkey -noout > {0}.pub".format("certs/cert%d" % i))

    from Crypto.PublicKey import RSA
    rsa = RSA.importKey(open("certs/cert%d.pub" % i).read())
    assert(rsa.e == 65537)
    ns.append(rsa.n)

from Crypto.Util.number import isPrime
from fractions import gcd

# pqs = [None] * len(ns)
# 
# for i in xrange(0, len(ns)):
#     for j in xrange(i + 1, len(ns)):
#         if gcd(ns[i], ns[j]) != 1:
#             c = gcd(ns[i], ns[j])
# 
#             for q in [i, j]:
#                 if ns[q] != c:
#                     if pqs[q] == None:
#                         pqs[q] = (c, ns[q] / c)
#                     else:
#                         l = []
#                         for e in pqs[q]:
#                             d = gcd(e, c)
#                             if d != 1:
#                                 l.extend([d, e/d])
#                             else:
#                                 l.append(e)
#                         pqs[q] = l
# for i, pq in enumerate(pqs):
#     if pq:
#         print(i, pq)
#         for e in pq:
#             print(isPrime(e))


import copy

col = set()
primes = copy.copy(ns)

change = True

while change:
    col = col | set(primes)
    change = False
    new_primes = []
    for i in xrange(len(primes)):
        for j in xrange(i + 1, len(primes)):
            assert(primes[i] != primes[j])
            d = gcd(primes[i], primes[j])
            if d != 1:
                new_primes.extend([primes[i] / d,  primes[j] / d, d])
                new_primes = set(new_primes)
                if 1 in new_primes:
                    new_primes.remove(1)
                new_primes = list(new_primes)

                change = True

    primes = new_primes
    col = col | set(primes)

col.add(0x33d6e3e93f724ea9cf1debb48039890fb32b46bbe08264ba821826152c6521d22d9b5109c96bc41d8ae5d86b1651be21b1886f57bd09fc6e6b22f28c37897d425L)
col.add(0x2c324c5b9f43b57a3910c3624f8f67a2deb5d4ed79d1516034f1f5b0a71fca40fd89ed01b468b2bca2e62b7e6f635e5b23394d16345a17a84d3481cc99764ae27L)

primes = []
for s in col:
    if isPrime(s):
        primes.append(s)

for i, n in enumerate(ns):
    l = []
    y = 1
    for p in primes:
        if n % p == 0:
            l.append(p)
            y *= p
    if y == n:
        print(i, l, n)

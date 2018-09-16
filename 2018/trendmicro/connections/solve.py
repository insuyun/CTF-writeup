p = 53436947781159654844791094883882513936770958579111494880684867268077018595158636811153470593268022602079608667531742837637180175896171948430428953584715049
q = 43440807593867497311250166633557882474138277411159911820971466913600375950238418974764035123301627429845877677401735552394932069631135117456122469665985573

import base64
dec = base64.urlsafe_b64decode('B24zu056rFEER1Y/QGPUoBlEuN801Zs78PV9Q7Xll0NfAVtkm2QWDRddhVBShrOQ/brjOtRRkgt8he7gtkL2Zf8HKYeCA++m0XsyNiCb035MtIMdcSsy/81Xy2sDTNz5nA3OkDfjUo1Uu8pISFuzMmZPe47yCbrmGLohKVpPUgd9')

from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse, isPrime, bytes_to_long, long_to_bytes

assert(isPrime(p) and isPrime(q))

import zlib
def inflate(data):
    decompress = zlib.decompressobj(
            16 + zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated

e = 65537L
phi = (p-1) * (q-1)
d = inverse(e, phi)
n = p * q
rsa = RSA.construct((n, e, d, p, q))

with open("key.inc", "wb") as f:
    f.write(dec)

with open("key.pem", "wb") as f:
    f.write(rsa.exportKey('PEM'))

#ie = int(dec.encode("hex"), 16)
ie = bytes_to_long(dec)
d = rsa.decrypt(ie)
d = long_to_bytes(d)

for i in xrange(256):
    ans = ""
    for j in xrange(len(d)):
        ans += chr((ord(d[j]) ^ i) % 256)

    print(ans)

import os
from base64 import b64decode
from sage.all import *

key64 = "Os9mhOQRdqW2cwVrnNI72DLcAXpXUJ1HGwJBANWiJcDUGxZpnERxVw7s0913WXNtV4GqdxCzG0pG5EHThtoTRbyX0aqRP4U/hQ9tRoSoDmBn+3HPITsnbCy67VkCQBM4xZPTtUKM6Xi+16VTUnFVs9E4rqwIQCDAxn9UuVMBXlX2Cl0xOGUF4C5hItrX2woF7LVS5EizR63CyRcPovMCQQDVyNbcWD7N88MhZjujKuSrHJot7WcCaRmTGEIJ6TkU8NWt9BVjR4jVkZ2EqNd0KZWdQPukeynPcLlDEkIXyaQx"

def get_dp_dq_qinv(key64):
    result = []
    key_tab = list(bytearray(b64decode(key64)))
    i = 0
    while i < len(key_tab):
        x = key_tab[i]
        if x == 0x02:  # integer start
            length = key_tab[i + 1]
            octets = key_tab[i + 2: i + 2 + length]
            value = int(str(bytearray(octets)).encode("hex"), 16)
            result.append(value)
            i += 2 + length
        else:
            i += 1
    return tuple(result)

# reference : https://eprint.iacr.org/2004/147.pdf
def recover_p_q(dp, dq):
    i = 0
    e = 65537
    dp1 = e * dp - 1
    dq1 = e * dq - 1
    for k in xrange(3, e):
        p, r = divmod(dp1, k)
        if r == 0:
            p += 1
            if p in Primes():
                for l in xrange(3, e):
                    q, r = divmod(dq1, l)
                    if r == 0:
                        q += 1
                        if q in Primes():
                            return p, q

if __name__ == '__main__':
    dp, dq, qinv = get_dp_dq_qinv(key64)
    p, q = recover_p_q(dp, dq)
    print("rsatool.py -p %d -q %d -o key.pem" % (p,q))
    print("openssl rsautl -decrypt -inkey key.pem -in flag.enc")

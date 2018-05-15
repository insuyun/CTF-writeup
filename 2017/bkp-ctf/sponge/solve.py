from hash import *

def get_xored():
    orig = '\xcb\xa5\xd1\x13\x9c4z<o\xc8\xaf\xcf\xec\xd2\x1a\x8d'
    mine = 'J/\xfb\x8bM\xcf\xb3\xc8\xe6\t\xaf\xcf\xec\xd2\x1a\x8d'
    xored = ""
    for i in xrange(16):
        xored += chr(ord(orig[i]) ^ ord(mine[i]))
    return xored[:10]

if __name__ == "__main__":
    GIVEN = 'I love using sponges for crypto'
    aes = AES.new('\x00'*16)
    plain = "0000071B88FBEC2CEBBE000000000000".decode("hex")[:10]
    plain += get_xored() + GIVEN[30:]

    h = Hasher()
    t1 = h.hash(plain)

    h = Hasher()
    t2 = h.hash(GIVEN)

    print(plain.encode("hex"))

P = 0x10000000000000000000000000000000000000000000000000000000000000425L

def str2num(s):
    return int(s.encode('hex'), 16)

def process(m, k):
    tmp = m ^ k
    res = 0
    for i in bin(tmp)[2:]:
        res = res << 1;
        if (int(i)):
            res = res ^ tmp
        if (res >> 256):
            res = res ^ P
    return res

def keygen(seed):
    #key = str2num(urandom(32))
    # key = 0x2a51d5b1bd1abdee4999363397902036332916fbce0982ebd3f5ece8e3ea3959
    key = 0xdb0f936a04210cac5d3166228b935bb5389f43e5876e733eec4ead96ec72d226L
    while True:
        yield key
        key = process(key, seed)

def str2num(s):
    return int(s.encode('hex'), 16)

with open("ciphertext", "r") as f:
    out = map(lambda x: int(x, 16), f.read().splitlines())

fake_secret1 = "I_am_not_a_secret_so_you_know_me"
fake_secret2 = "feeddeadbeefcafefeeddeadbeefcafe"
secret = 0x472cab91ceb46abd08b68a856ca8ec6e156861ea1f186f21f356ad8bfde06b10L
generator = keygen(secret)
print(hex(out[0] ^ 0xdb0f936a04210cac5d3166228b935bb5389f43e5876e733eec4ead96ec72d226L)[2:-1].decode("hex"))
print("%x" % generator.next())
print("%x" % generator.next())
print ("%x" % (str2num(fake_secret1) ^ out[1]))
print ("%x" % (str2num(fake_secret2) ^ out[2]))


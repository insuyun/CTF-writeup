import commands
from pwn import *

gdb = """b *main
r encrypt key.bin input output
set $rip=encrypt-0x8A0+0x700
set $rdi = {{RDI}}
set $rsi = {{RSI}}
b *(encrypt-0x8A0+0x873)
c
info reg $rax
q"""

cipher = "3f29 4317 e51e 932a a1c0 52b7 94f7 86e4 277d 5948 dd43 ab45 7f6b ae56 09e7 3aec 670e 5d3d 0b90 e42c 2e03 03bc d2e3 d0bb".replace(" ", "").decode("hex")

k = []
k.append(u64("83a6fa4409377170".decode("hex")))
k.append(u64("92e55b2fe96f930c".decode("hex")))

def to_blocks(x):
    assert(len(x) % 16 == 0)
    blks = []
    for i in xrange(0, len(x), 16):
        d = []
        for j in xrange(2):
            d.append(u64(x[i + 8*j:i + 8*j + 8]))
        blks.append(d)
    return blks

def f(x, y):
    gdb_ = gdb.replace("{{RDI}}", str(x))
    gdb_ = gdb_.replace("{{RSI}}", str(y))
    with open("gdb-script", "wb") as f:
        f.write(gdb_)
    out = commands.getoutput("gdb -x gdb-script ./cipher").splitlines()[-1]
    out = int(out.split("\t")[1], 16)
    #print("out : %16X\n" % out)
    return out

def getk(i):
    if len(k) <= i or k[i] is None:
        prev = getk(i - 2)
        #assert(len(k) == i)
        while len(k) <= i:
           k.append(None)
        k[i] = f(prev, 0x9104F95DE694DC50)
    return k[i]

# Li+1 = Ri
# Ri+1 = Li ^ F(Ri, Ki)

# Ri = Li+1
# Li = Ri+1 ^ F(Li, Ki)

# getk(14)
blks = to_blocks(cipher)
for i in xrange(0, len(blks)):
    l, r = blks[i]
    l, r = r, l

    for j in xrange(14):
        l,r = r,l
        ks = getk(14 - j - 1)
        l ^= f(r, ks)
    print(p64(r) + p64(l))
#getk(2)
print(map(lambda x:hex(x), k))

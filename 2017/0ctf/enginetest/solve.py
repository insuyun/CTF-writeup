from z3 import *
from pwn import *
size = 0x8717
indicies = []

def read_qword(f):
    d = f.read(8)
    if not d:
        return None
    else:
        return u64(d)

def read_struct(f):
    a = []
    for i in xrange(5):
        r = read_qword(f)
        if r is None:
            return
        a.append(r)
    return a

def get_or_create(mapping, n):
    if not n in mapping:
        mapping[n] = Bool("b_%d" % n)
    return mapping[n]

with open("indicies", "rb") as f:
    while True:
        r = read_qword(f)
        if r is None:
            break
        indicies.append(r)

opcodes = []
with open("opcode", "rb") as f:
    while True:
        s = read_struct(f)
        if s is None:
            break
        opcodes.append(s)

op = []
with open("op", "rb") as f:
    r = read_qword(f) #skip first
    while True:
        r = read_qword(f)
        if r is None:
            break
        op.append(r)

ip = []
with open("ip", "rb") as f:
    r = read_qword(f) #skip first
    while True:
        r = read_qword(f)
        if r is None:
            break
        ip.append(r)

s = Solver()
mapping = {}
b_0 = get_or_create(mapping, 0)
b_1 = get_or_create(mapping, 1)
s.add(b_0 == False)
s.add(b_1 == True)

for i in xrange(size):
    idx = indicies[i]
    mode, op1, op2, op3, dst = opcodes[idx]

    if i % 0x1000 == 0:
        print("DONE: %x" % i)
    if mode == 1:
        b_dst = get_or_create(mapping, dst)
        b_op1 = get_or_create(mapping, op1)
        b_op2 = get_or_create(mapping, op2)
        f = (b_dst == And(b_op1, b_op2))
        #print(f)
        s.add(f)
    elif mode == 2:
        b_dst = get_or_create(mapping, dst)
        b_op1 = get_or_create(mapping, op1)
        b_op2 = get_or_create(mapping, op2)
        f = (b_dst == Or(b_op1, b_op2))
        #print(f)
        s.add(f)
    elif mode == 3:
        b_dst = get_or_create(mapping, dst)
        b_op1 = get_or_create(mapping, op1)
        b_op2 = get_or_create(mapping, op2)
        f = (b_dst == Xor(b_op1, b_op2))
        #print(f)
        s.add(f)
    elif mode == 4:
        b_dst = get_or_create(mapping, dst)
        b_op1 = get_or_create(mapping, op1)
        b_op2 = get_or_create(mapping, op2)
        b_op3 = get_or_create(mapping, op3)
        f = (b_dst == If(b_op1 == True,  b_op2, b_op3))
        #print(f)
        s.add(f)

s.check()
m = s.model()

v = ""
out = ""
for idx in op:
    if is_true(m[get_or_create(mapping, idx)]):
        v = "1" + v
    else:
        v = "0" + v

    if len(v) == 8:
        out += chr(int(v, 2))
        print("out: %s" % out)
        v = ""

# not start with W
f = False
for i, idx in enumerate(op):
    v = get_or_create(mapping, idx)
    f = Or(f, Distinct(v, m[v]))

print(f)
s.add(f)

print(s.check())
m = s.model()
v = ""
out = ""
for idx in op:
    if is_true(m[get_or_create(mapping, idx)]):
        v = "1" + v
    else:
        v = "0" + v

    if len(v) == 8:
        out += chr(int(v, 2))
        print("out: %s" % out)
        v = ""

out = ""
for idx in ip:
    if is_true(m[get_or_create(mapping, idx)]):
        v = "1" + v
    else:
        v = "0" + v

    if len(v) == 8:
        out += chr(int(v, 2))
        print("out: %s" % out)
        v = ""

# flag{wind*w(s)_*f_B1ll(ion)_g@t5s}



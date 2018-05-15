from z3 import *

"""
m: 66dae1eed04738e5b515a45e1d2800a801f0b5004fe48b51a162798c051519c0
tmp: 7bb808fb1265984d474c53f7c4961c96091d4612e85ea30c00318ed647478a1
res: 43fdacf910180abdf16186922d28061f2706a21e5720baa7be434827d42f5964
"""
m_val = BitVecVal(0x66dae1eed04738e5b515a45e1d2800a801f0b5004fe48b51a162798c051519c0, 256)
#tmp_val = BitVecVal(0x7bb808fb1265984d474c53f7c4961c96091d4612e85ea30c00318ed647478a1, 256)
res_val = BitVecVal(0x43fdacf910180abdf16186922d28061f2706a21e5720baa7be434827d42f5964, 256)
P = BitVecVal(0x10000000000000000000000000000000000000000000000000000000000000425L, 256)

s = Solver()
m = BitVec("m", 256)
k = BitVec("k", 256)
res = []

tmp = m ^ k
#s.add(tmp == tmp_val)
res.append(BitVec("res_0", 256))
s.add(res[0] == BitVecVal(0, 256))
for i in xrange(256):
    c1 = (Extract(255 - i, 255 - i, tmp) == BitVecVal(1, 1))
    c2 = (Extract(255, 255, res[i]) == BitVecVal(1, 1))

    res.append(BitVec("res_%d" % (i + 1), 256))
    s.add(res[i + 1] == If(c1,
        If(c2, (res[i] << 1) ^ tmp ^ P, (res[i] << 1) ^ tmp),
        If(c2, (res[i] << 1) ^ P, (res[i] << 1))))

s.add(res[256] == res_val)
print(s.check())
print("k=%s" % s.model()[k])

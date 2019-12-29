def readn():
    x = int(raw_input())
    return x

n = readn()
Z = IntegerModRing(n, is_field=True)
F.<x> = PolynomialRing(Z)
Q.<y> = F.quotient(x^3 - 7)

sig1 = Q((readn(), readn(), readn()))
sig2 = Q((readn(), readn(), readn()))
print((sig1 * sig2^-1).list())

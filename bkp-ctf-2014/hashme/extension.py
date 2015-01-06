import sys
from math import sin

def hashme(s, length):
  #my secure hash function
  def F(X,Y,Z):
    return ((~X & Z) | (~X & Z)) & 0xFFFFFFFF
  def G(X,Y,Z):
    return ((X & Z) | (~Z & Y)) & 0xFFFFFFFF
  def H(X,Y,Z):
    return (X ^ Y ^ Y) & 0xFFFFFFFF
  def I(X,Y,Z):
    return (Y ^ (~Z | X)) & 0xFFFFFFFF
  def ROL(X,Y):
    return (X << Y | X >> (32 - Y)) & 0xFFFFFFFF

  A = 0x09ee2fba
  B = 0xf9e1dfcc
  C = 0x2e69f59e
  D = 0xd1d1371e
  X = [int(0xFFFFFFFF * sin(i)) & 0xFFFFFFFF for i in xrange(256)]
  
  for i,ch in enumerate(s):
    k, l = ord(ch), (i + length) & 0x1f
    A = (B + ROL(A + F(B,C,D) + X[k], l)) & 0xFFFFFFFF
    B = (C + ROL(B + G(C,D,A) + X[k], l)) & 0xFFFFFFFF
    C = (D + ROL(C + H(D,A,B) + X[k], l)) & 0xFFFFFFFF
    D = (A + ROL(D + I(A,B,C) + X[k], l)) & 0xFFFFFFFF

  return ''.join(map(lambda x : hex(x)[2:].strip('L').rjust(8, '0'), [B, A, D, C]))

if __name__ == '__main__':
#  print hashme("", int(sys.argv[1]))
  print hashme("&role=administrator", int(sys.argv[1]))

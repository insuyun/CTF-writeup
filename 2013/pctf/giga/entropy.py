import sys
import os
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
import SocketServer
import threading
import time

rbuf = os.urandom(4096)
hr = MD5.new()

def rng(n):
  global rbuf
  rand = rbuf[:n]
  rbuf = rbuf[n:]
  while (len(rbuf) < 4096):
    hr.update(os.urandom(4096))
    rbuf += rbuf + hr.hexdigest()
  return rand

collections = []

for x in xrange(100000):
	rsa = RSA.generate(1024,rng)
	p = getattr(rsa, 'p')
	q = getattr(rsa, 'q')

	if p in collections or q in collections:
		print "FAIIIIIIIIIIIIL"
		sys.exit()
	
	collections.append(p)
	collections.append(q)

	if x % 1000 == 0:
		print "%d times" % x


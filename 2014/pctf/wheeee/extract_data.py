import random,commands
from socket import *


def generate():
	# payload for verifying result
	payload = ""
	for i in xrange(0, 0xfff):
		payload += "000%03x" % i

	return payload

payload = generate()
print len(payload)
f = open('result', 'a')
block_size = 1026

for x in xrange(0, len(payload), block_size):
	s = socket(AF_INET, SOCK_STREAM)
	s.connect(('54.82.75.29', 8193))
	print s.makefile().readline()
	seed = s.makefile().readline()[31:47]
	print "seed : %s" % seed
	result = commands.getstatusoutput('./crack %s' % seed)[1]
	if (result == ''):
		s.close()
		x -= block_size
		continue
	print "result : %s" % result
	s.send(result+"\n")
	print s.makefile().readline()
	print s.makefile().readline()
	print payload[x:x+block_size]
	s.send(payload[x:x+block_size]+"\n")
	encrypted = s.recv(block_size + 1).rstrip()
	encrypted += "0" * (block_size - len(encrypted))
	print "input : %d, output : %d" % (len(payload[x:x+block_size]), len(encrypted))
	f.write(encrypted+"\n")
	print encrypted
	s.close()

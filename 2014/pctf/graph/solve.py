import os,random,math,pickle,zlib
def intract(n):
  s = []
  while n > 0:
    s.append(chr(n & 0xff))
    n = n >> 8
  return ''.join(s[::-1])

d = open('ciphertext','r').read().decode("base64")
ct = pickle.loads(zlib.decompress(d))

pub = open('pubkey', 'r')
pub = ''.join(pub.readlines()[1:-1])

pk = pickle.loads(zlib.decompress(pub.decode("base64")))
pubkey = pk['pub']
keylen = len(pubkey)

pubkey_sorted = sorted(pubkey, key=lambda x:len(x))
limit = len(pubkey_sorted[63])

privkey = []
for i in xrange(len(pubkey)):
	if (len(pubkey[i]) <= limit):
		privkey.append(i)
	
print privkey
print intract(reduce(lambda a,b:a+b,[ct[i] for i in privkey]))

from Crypto.Cipher import AES
import base64, struct, sys

table = {}

m1 = base64.b64decode("QUVTLTI1NiBFQ0IgbW9kZSB0d2ljZSwgdHdvIGtleXM=")[0:16]
e1 = base64.b64decode("THbpB4bE82Rq35khemTQ10ntxZ8sf7s2WK8ErwcdDEc=")[0:16]
m2 = base64.b64decode("RWFjaCBrZXkgemVybyB1bnRpbCBsYXN0IDI0IGJpdHM=")[0:16]
e2 = base64.b64decode("01YZbSrta2N+1pOeQppmPETzoT/Yqb816yGlyceuEOE=")[0:16]
target = base64.b64decode("s5hd0ThTkv1U44r9aRyUhaX5qJe561MZ16071nlvM9U=")

def give_key(i):
	key = "\x00"*29 + struct.pack('>I', i)[1:]
	return key

brute_range = 0xffffff

for i in xrange(brute_range):
		key = give_key(i)
		cipher = AES.new(key)
		table[cipher.encrypt(m1)] = i
		if i % 0x10000 == 0:
			print hex(i)

print "[*] Constructing a table is completed."

for i in xrange(brute_range):
		key = give_key(i)
		cipher = AES.new(key)
		decrypted_text = cipher.decrypt(e1)
		if table.has_key(decrypted_text):
				key1 = key
				key2 = give_key(table[decrypted_text])

				print "[*] key1 : " + repr(key1)
				print "[*] key2 : " + repr(key2)

				c1 = AES.new(key1)
				c2 = AES.new(key2)

				if (c1.decrypt(e2) != c2.encrypt(m2)):
						continue

				print "[*] Answer : " + c2.decrypt(c1.decrypt(target))

		if i % 0x10000 == 0:
			print hex(i)

import math 
#from PrimeUtils import PrimeUtils
from Crypto.Util import number

class PrivKey:
	def __init__(self, p, q, n):
		self.p = p
		self.q = q
		self.n = n
		self.l = (p-1)*(q-1)
		#self.m = PrimeUtils.modinv(self.l, self.n)
		self.m = number.inverse(self.l, self.n)

class PubKey:
	def __init__(self, n):
		self.n = n
		self.n_sq = n * n
		self.g = n + 1

class PKI:
	def __init__(self, pubkey = None, privkey = None):
		if pubkey != None:
			self.pubkey = pubkey
			self.privkey = privkey
		else:
			(self.pubkey, self.privkey) = self.gen_keypair(512)

		self.r = None

	def encrypt(self, plain):
		if self.pubkey == None:
			assert AssertionError, 'Public key must be exist'
			raise
		
		pubkey = self.pubkey
		while True:
			r = number.getPrime(int(round(math.log(pubkey.n, 2))))
			if not r > 0:
				continue

			if r > pubkey.n:
				continue
			break

		cipher = pow(pubkey.g, plain, pubkey.n_sq) * pow(r, pubkey.n, pubkey.n_sq) % pubkey.n_sq
		return cipher

	def decrypt(self, cipher):
		if self.privkey is None:
			assert AssertionError, 'Private key must be exist'
			raise
	
		if self.pubkey is None:
			assert AssertionError, 'PubKey key must be exist'
			raise

		privkey = self.privkey
		pubkey = self.pubkey
		
		plain = (privkey.m * ((pow(cipher, privkey.l, pubkey.n_sq) - 1) // pubkey.n)) % pubkey.n
		return plain

	def gen_keypair(self, bits):
		#p = PrimeUtils.get_prime(bits//2)
		p = number.getPrime(bits//2)
		#q = PrimeUtils.get_prime(bits//2)
		q = number.getPrime(bits//2)


		n = p*q
		return (PubKey(n), PrivKey(p,q,n))

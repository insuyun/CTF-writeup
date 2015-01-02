import socket, struct, sys, binascii, PKI
from PKI import PubKey, PrivKey, PKI

g_guestkey = '\xe1\xe7\xac\xa9\x19c\x0c\xf0'
g_pki_client = PKI()
g_pki_server = PKI()
s = None  
with_encryption = False

def s2i(s):
	return int(s.encode("hex"),16)

def i2s(s):
	s = hex(s)[2:]
	if (s[-1] == "L"):
		s = s[:-1]
	if len(s) % 2 == 1:
		s = "0" + s
	return s.decode("hex")

def create_socket(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	return s

def exchange_key():
	global with_encryption
	print s.recv(1024)
	write(hex(g_pki_client.pubkey.n))
	data = read()[2:]
	data = data[:-1]
	print data
	n = int(data, 16)
	with_encryption = True
	return PubKey(n)

def write(data, exploit = False):
	global with_encryption
	if with_encryption and not exploit:
		data = i2s(g_pki_server.encrypt(s2i(data)))

	size = struct.pack('<I', len(data))
	send_data = size + data
	s.send(send_data)

def read():
	size_str = s.recv(4)
	size_str = struct.unpack('<I', size_str)[0]
	data = s.recv(size_str)


	if with_encryption:
		data_int = s2i(data)
		data = i2s(g_pki_client.decrypt(data_int))
	return data

def read_files(filenames, authkey):
	cmd = 'cat '
	for filename in filenames:
		cmd += filename + ' '

	cmd = cmd.rstrip() + "\n"
	write(authkey + cmd)
	res = ''
	for _ in range(len(filenames)):
		res += read()
	return res

def exploit():
	n = 0x86e05276d3c364cd6157e23cd972e0a662dff9ebf9ade83eae022c292c767bcd6cf528c7f6ae98af2f7811d99c9e45e7e4e6f1b9841aabf89a84dd0673099b61L
	secret = s2i("\x1f\x59\x85\x6d\xbb\xbe\x90\x99\x5c\xf9\x49\x75\xaf\xd9\x4d\xcf\x46\xbf\x2d\x16\xd8\xb8\xa3\x75\x46\x85\xd3\xeb\x37\x65\xd6\x91\x84\x62\x37\x8a\x2f\x7e\x94\x81\x82\xe8\x4a\x85\x7a\x25\xbe\x05\x7a\x12\x2e\x9d\x65\xe3\x2f\xb0\x1a\x98\x4f\x44\x2e\x78\x1f\xa0\x2e\x8a\x4d\x27\x28\xb1\xa4\xc3\xea\x39\x05\xaa\x95\xab\x9f\xba\x7b\x7d\xfa\x3b\x39\x11\x6d\x49\xc1\x0d\x16\x17\x25\xaa\x0b\xee\xac\x18\xb7\xa2\xa9\xc9\xd5\x5a\x0b\xf6\xf1\xa2\xb2\xca\x90\x3e\xb1\x50\x86\x99\x5b\x2f\x77\xd7\x7d\x3f\x01\x67\x87\x08\xee\x60")
	plain1 = s2i("secret\n")
	plain2 = s2i("flag2\n\n")
	new_plain = i2s((secret + ((plain2 - plain1) * ((secret * n) % (n*n)))) % (n*n))
	write(new_plain, True)

	res = ''
	res = read()
	return res

if (len(sys.argv) < 4):
	print "Argument is too short"
	exit(-1)

host = sys.argv[1]	
port = int(sys.argv[2])
filename = sys.argv[3]

if (len(sys.argv) >= 5):
	key = sys.argv[4]
else:
	key = g_guestkey

s = create_socket(host, port)
g_pki_server = PKI(exchange_key())
print exploit()


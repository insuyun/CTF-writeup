"""
Treasure Island:04250:2:7888
Gulliver's Travels:30984:1:5597
Alice in Wonderland:61142:3:1703
"""
with open('fileidx', 'r') as f:
    data = f.read()

fileidx = ''.join(map(lambda x:chr(int(x,2)), [data[i:i+8] for i in xrange(0, len(data), 8)]))
print(fileidx)

with open('04250', 'rb') as f:
    data = f.read()

b = bytearray(data)
for i in xrange(len(b)):
    b[i] >>= 1
print(b)

with open('30984', 'rb') as f:
    data = f.read()
b = bytearray(data)
for i in xrange(len(b)):
    b[i] &= 0x7f
print(b)

x = """CB FD 3F BE DA 05 03 B7  FF FE 73 34 53 30 CE 34
B4 7E C7 66 13 76 BD 4F  94 FA 6D 9A 82 90 43 E5
A9 21 9F A8 0B 5D 36 35  81 CD 32 84 01 48 0B 1D
CC 9D E0 B8 A0 66 BE C9  6D CD E3 DC 7F 5D 1A C1
E4 78 09 E6 F4 DF 9A 2F  59 04 C1 44 86 2B 80 27
9C B7 67 BD 7D A5 B9 6A  FA 8E 66 CB 69 92 13 64
6A A7 F3 9B 8E 40 DD 76  21 EC E3 B6 6C DB CB 0F
E0 C5 68 52 06 C3 05 29  29 2E 9F 82 50 16 F4 63
5A CB F4 0C 7F D0 E9 F2  D2 98 FD D6 C0 59 DC E4
99 8E 2C 3D 32 B0 17 C6  1A 15 5F 78 40 A2 16 B3
B4 30 F4 55 D9 42 C3 E1  43 C3 40 56 29 EA 31 F1
D0 1D 25 F6 C2 CC 86 50  B4 2F B8 A7 AA 76 83 52
47 51 7E 05 99 DD 90 FF  79 14 4F CC D5 4A B4 38
8E 3A C7 7B DA 47 F8 1E  81 A0 37 F4 DA E4 00 3D
5A 2F E6 AC 50 21 B4 00  6E 15 64 D6 69 40 D2 B1
16 E4 3B FB 0A 0F F4 97  83 00 F9 3D 7F 5B 60 CE"""
x = bytearray(x.replace("\n", "").replace(" ","").decode("hex"))
print(hex(x[0]))
with open('61142', 'rb') as f:
    data = f.read()

b = bytearray(data)
t = 0
for i in xrange(len(b)):
    b[i] ^= x[t]
    t = b[i]
print(b)


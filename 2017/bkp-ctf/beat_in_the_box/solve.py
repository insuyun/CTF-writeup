data = "GLI|nuXdfkXfmt)Ximf~Xjrtndz\x00"
print(len(data))
value = 0x3077C534 - 0x3077C4FC

for v3 in xrange(value):
    for v4 in xrange(value):
        #if v3 + 8 * v4 != value:
        #    continue

        new_data = bytearray(data[:])
        for i in xrange(0x1c):
            new_data[i] = ((new_data[i] ^ v3) + v4) % 0x100
        print(repr(new_data))

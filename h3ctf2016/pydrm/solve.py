b = [0x87, 0x9a, 0x92, 0x8e, 0x8b, 0x85, 0x8b, 0x96, 0x81, 0x8b, 0x95, 0x81,
        0x84, 0x87, 0x96, 0x96, 0x87, 0x94, 0x81, 0x96, 0x8a, 0x83, 0x90, 0x81,
        0x8b, 0x8f, 0x92, 0x8e, 0x8b, 0x85, 0x8b, 0x96]
c = []
for d in b:
    c.append(chr(d-34))

print(''.join(c))

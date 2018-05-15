"""
if op == 153:
    op = dis.opmap["LOAD_CONST"]
if op == 136:
    op = dis.opmap["MAKE_FUNCTION"]
if op == 145:
    op = dis.opmap["STORE_NAME"]
if op == 134:
    op = dis.opmap["IMPORT_NAME"]
if op == 83:
    op = dis.opmap["RETURN_VALUE"]
if op == 97:
    op = dis.opmap["LOAD_FAST"]
if op == 104:
    op = dis.opmap["STORE_FAST"]
if op == 70:
    op = dis.opmap["BINARY_MULTIPLY"]
if op == 39:
    op = dis.opmap["BINARY_ADD"]
if op == 155:
    op = dis.opmap["LOAD_GLOBAL"]
if op == dis.opmap["DELETE_ATTR"]:
    op = dis.opmap["LOAD_ATTR"]
"""

import rotor

def encrypt(data):
    key_a = '!@#$%^&*'
    key_b = 'abcdefgh'
    key_c = '<>{}:"'
    secret = key_a * 4 + '|' + (key_b + key_a + key_c) * 2 + '|' + key_b * 2 + 'EOF'
    rot = rotor.newrotor(secret)
    return rot.encrypt(data)


def decrypt(data):
    key_a = '!@#$%^&*'
    key_b = 'abcdefgh'
    key_c = '<>{}:"'
    secret = key_a * 4 + '|' + (key_b + key_a + key_c) * 2 + '|' + key_b * 2 + 'EOF'
    rot = rotor.newrotor(secret)
    return rot.decrypt(data)

with open("encrypted_flag", "rb") as f:
    data = f.read()

print(repr(decrypt(data)))

# flag{Gue55_opcode_G@@@me}

def rol(s, x):
  return (s << x | s >> (32 - x)) & 0xffffffff

def decrypt(s, a, b):
  result = ""
  for i in range(0, len(s), 2):
    result += chr( (a ^ ord(s[i])) & 0xff)
    a = rol(a, 5) ^ 0x2f;
    result += chr( (b ^ ord(s[i+1])) & 0xff)
    b = (a & 0xff) ^ rol(b, 11)

  return result

s = "\x0F\x8E\x9E\x39\x3D\x5E\x3F\xA8\x7A\x68\x0C\x3D\x8B\xAD\xC5\xD0\x7B\x09\x34\xB6\xA3\xA0\x3E\x67\x5D\xD6"

logs = open('logs').readlines()[1:]

for log in logs:
  log = log.rstrip()
  arg = log.split(" ")[-3: -1]
  print decrypt(s, int(arg[0]), int(arg[1]))

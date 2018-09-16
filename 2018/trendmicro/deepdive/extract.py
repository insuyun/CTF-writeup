f = open("many(8).php", "rb").read()
start = f.index("mausoleum.jpg")
start = f.index("PK", start)
end = f.index("------WebKitFormBoundary", start)

open("mausoleum.exe", "wb").write("MZ" + f[start+2:end-2])

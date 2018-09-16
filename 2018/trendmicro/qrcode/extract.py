from PIL import Image
im = Image.open("qrcode.png")
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

def white(pixel):
    return (not (pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255)
            and (pixel[0] > 200 and pixel[1] > 200 and pixel[2] > 200))

def black(pixel):
    return pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0

# 28 x 29

# 455 x 107

sx = 107
sy = 455 - 28 * 12

for x in xrange(25):
    for y in xrange(25):
        nb = nw = 0
        for i in xrange(29):
            for j in xrange(28):
                pixel = pixels[sx+i+x*29][sx+j+y*28]
                if white(pixel):
                    nw += 1
                if black(pixel):
                    nb += 1

        cell = "?"
        if nb > 400:
            cell = "X"
        if nw > 400:
            cell = "_"
        import sys
        sys.stdout.write(cell)
    print

# side = 20
# 
# for i in xrange(width - side):
#     for j in xrange(height - side):
#         colors = []
# 
#         # check all 0
#         for x in xrange(i, i + side):
#             for y in xrange(j, j + side):
#                 if pixels[x][y] == (0, 0, 0):
#                     print(x, y)

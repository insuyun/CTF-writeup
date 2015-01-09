#!/usr/bin/env python

from PIL import Image
import random

def get_color(x, y, r):
  n = (pow(x, 3) + pow(y, 3)) ^ r
  return (n ^ ((n >> 8) << 8 ))

flag_img = Image.open('enc.png.orig')
im = flag_img.load()
r = random.randint(1, pow(2, 256))
print flag_img.size

enc_img = Image.new(flag_img.mode, flag_img.size)
enpix = enc_img.load()

for x in range(flag_img.size[0]):
  for y in range(flag_img.size[1]):
    enpix[x,y] = 0

for x in range(flag_img.size[0]):
  for y in range(flag_img.size[1]):
    enpix[x, y] = im[x,y] ^ get_color(x, y, 0)

enc_img.save('enc' + '.png')



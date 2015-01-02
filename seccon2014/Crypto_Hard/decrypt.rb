#encoding BINARY
require 'openssl'

def parse_input input
  input.scan(/.{7}/m).map{|v| string_to_int(v)}
end

def string_to_int string
  num = 0
  string.each_byte do |elem|
    num = (num << 8) + elem
  end
  num
end

#based on pseudo code from http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Iterative_method_2 and from translating the python implementation.
def extended_gcd(a, b)
  last_remainder, remainder = a.abs, b.abs
  x, last_x, y, last_y = 0, 1, 1, 0
  while remainder != 0
    last_remainder, (quotient, remainder) = remainder, last_remainder.divmod(remainder)
    x, last_x = last_x - quotient*x, x
    y, last_y = last_y - quotient*y, y
  end

  return last_remainder, last_x * (a < 0 ? -1 : 1)
end

def invmod(e, et)
  g, x = extended_gcd(e, et)
  if g != 1
    raise 'Teh maths are broken!'
  end
  x % et
end

p = (0x1000000 * 0x1000000) + 21
x = 2

=begin
data =  parse_input "00ee 23ed c816 9000 983f b74d 0284"
key = data[0]
enc = data[1]

s = key.to_bn.mod_exp(2, p).to_i
s = invmod(s, p)
s = (enc * s ) % p
p s.to_s(16)
=end

=begin
k=20
loop do
  if (7776.to_bn.mod_exp(k, p).to_i == 69219086192344)
    puts "[*] I FOUND KEY : %d\n" % k
    break
  end
  k += 1
end
=end

x = 9999
#f = open("gg.bin", "rb").read()
f = open("eflag.bin", "rb").read()

data = parse_input(f)
key = data[0]
#data = data.slice!(1,10)
data = data.slice!(1, data.length)
s = key.to_bn.mod_exp(9999, p).to_i
s = invmod(s, p)

fo = open("flag.png", "wb")
#fo = open("gg_d.png", "wb")

data.each do |d|
  x = "%012X" % ((d*s) % p)
  fo.write([x].pack('H*'))
end
fo.close()

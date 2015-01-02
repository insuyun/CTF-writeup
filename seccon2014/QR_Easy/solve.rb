=begin
def calc_bch num
  orig = num
  num = num << 10
  bch = 2**10 + 2**8 + 2**5 + 2**4 + 2**2 + 2 + 1
  while (num >= bch)
    bit_length = num.to_s(2).length - 1
    num ^= (bch << (bit_length - 10))
  end
  num = (orig << 10) + num
  num ^= 0b101010000010010
  "%015B" % num
end

8.times do |x|
  guess = ("10" + "%03B" % x).to_i(2)
  if calc_bch(guess)[-8..-1] == "10111110"
    puts "[*] Mask pattern : %03B" % x 
  end
end
=end

d = [0]
d[1] = '00100000'
d[2] = '00110100'
d[3] = '11111010'
d[4] = '01000101'
d[5] = '00010001'
d[6] = '00111101'
d[7] = '00000100'
d[8] = '10011110'
d[9] = '11010100'
d[10] = '00010100'
d[11] = '11011101'
d[12] = '11010010'
d[13] = '01010100'
d[14] = '01001110'
d[15] = '01011001'
d[16] = '00001110'
d[17] = '01010001'
d[18] = '11011010'
d[19] = '10010010'
d[20] = '11010101'
d[21] = '00011001'
d[22] = '00010001'
d[23] = '00001110'
d[24] = '00010010'
d[25] = '00011111'
d[26] = '01000000'
d = d.slice(1, d.length)

input = "00100000
00110100
11111010
01000101
00010001
00111101
00000100
10011110
11010100
00010100
11011101
11010010
01010100
01001110
01011001
00001110
01010001
11011010
10010010
11010101
00011001
00010001
00001110
00010010
00011111
01000000".split("\n")

input.length.times do |i|
  puts "[*] Diff(%d) : %s %s" % [i, d[i], input[i]] if  d[i] != input[i]
end

input = input.join
type = input.slice!(0,4)
len = input.slice!(0,9).to_i(2)
encode = input.slice!(0, 11*3)
dict = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] + ("A".."Z").to_a + [" ","$", "%","*","+","-",".","/", ":"]
lookup = {}

dict.length.times do |i|
  dict.length.times do |j|
    lookup[45*i + j] = dict[i]+dict[j]
  end
end
encode = encode.scan(/.{11}/).map{|v| v.to_i(2)}
#input = [564, 1051, 1225, 1333]
encode = encode.map do |x|
  lookup[x]
end

type = input.slice!(0,4)
len = input.slice!(0,8).to_i(2)
p encode.join + input.scan(/.{8}/).map{|v| v.to_i(2).chr}.join



require 'bigdecimal'

def string_to_int string
  num = 0
  string.split.each do |x|
    num = (num << 8) + x.to_i(16)
  end
  num
end


n = "fd 7f c4 9e 20 04 f3 b7 ee 67 c3 6f 7a 86 c8 0a 2e fe e0 39 0c 58 1f bd 4d 74 5d 93 95 b5 98 a2 ee 08 bd 5d 33 7e 97 e8 09 84 56 6c 2c 85 3e f6 3e cc 82 b4 94 50 81 ac 16 eb e6 27 c2 91 6f 96 59 fb 09 91 30 46 e4 35 41 25 76 ad 9d 0b a1 de 4e 8d 99 a4 b2 90 1e b0 af 70 d5 ac 99 ab 30 cf 65 21 2c 50 6e b1 26 c1 8e 06 87 51 15 52 4f a6 a8 af fc 15 b3 d9 9a 32 5e 22 e1 f3 54 b0 cf 6a 9a c8 d7 d7 af 2a ee 29 c2 46 16 32 e3 70 c4 22 c1 22 fb f5 81 d0 71 ec 5b 71 39 de b7 83 57 47 45 b9 6f 40 6b cb c9 d7 d8 18 1b 4a e6 ba ee 0e d3 f3 30 18 ef b9 dd ca 42 92 dd 08 a9 dd ed 9e d7 ca 79 d1 38 d5 1d 5d aa 4a ea 6a 8d 60 04 88 5a 6c eb 8a 63 02 89 9c e4 97 d2 63 e8 56 c9 8e de a3 ab 9d 68 72 68 21 ed e3 49 e4 53 ba dd a2 69 f2 0c ec a5 85 9c 44 c9 d6 c4 3f 9c 11 00 5e 3d cf 35 53 08 f0 88 1b 2a 80 49 1c 33 4d fa 86 b9 e5 cf 8d 8a 88 6c 74 f3 0b f7 df 8d 59 9f d9 3b 33 a3 38 6a 0c e4 99 9d d0 89 26 bf 0d 49 66 aa 7e 52 bd d3 ff 7d 1b 68 7b b9 37 bd bc 19 f1 d8 02 58 a1 ff e9 b8 e7 d4 c4 d3 b3 e8 08 0d 82 98 94 35 e0 79 bf 14 2a 07 6d 88 6d f8 f2 a7 ff 7f 5b 4c c1 f4 7c ee a8 9f 14 7d 6d 31 f0 8c f3 09 8a e6 f9 a6 c6 ee 77 29 b3 60 29 7e 6e f4 6c 92 66 35 eb 94 5a 6c 4f 2e 8f b7 cc 72 c5 33 cd 1f 8b ed 90 28 c2 63 eb dd 7c ab 19 b2 94 9f 81 61 8e c9 e0 00 83 99 69 89 02 2a 83 56 e8 6a 18 5f 09 f3 59 05 63 41 fa 92 2f bf 19 cf 48 05 36 53 47 9e 9e 28 60 30 b4 7b 8c 62 89 c5 c9 14 96 0b 2b 20 35 b2 da f0 1b 8f e5 38 25 89 89 81 e7 7b ac 85 bc 1e 79 57 7d af 12 32 fe e8 ef 4a 3e ba 23 ca 85 4b 2d e4 89 8a e0 5d 41 cb 43 ee 53"

n = string_to_int(n)

root_n = BigDecimal(n.to_s).sqrt(2000).to_i
prev = n % root_n
loop do
  root_n += 1
  if (n % root_n) == 0
    puts "[*] Got factor! : %d" % root_n
    break
  end
#  readline
end

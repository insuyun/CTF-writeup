require 'socket'

class Exploit
  def initialize
    @s = TCPSocket.new('localhost', 4567)
    p @s.readline
    p @s.readline
  end

  def query(msg)
    @s.write(msg + "\n")
    res = @s.readline
    return !res.index("padding")
  end

  def sxor(s1, s2)
    s1.bytes.zip(s2.bytes).map{|v| (v[0] ^ v[1]).chr}.join
  end

  def brute
    orig = "a" * 32 # initial value
    plain = "\x00" * 16

    16.times do |i|
      index = 15 - i  # find value from backward
      p index
      padding_byte = i + 1

      msg = sxor(orig[0..15], plain)
      padding = (padding_byte.chr * i).rjust(16, "\x00")
      msg = sxor(msg, padding) + orig[16..-1]

      puts "Padding : #{padding.inspect}"
      puts "MSG : #{msg.inspect}"

      256.times do |g|
        msg[index] = (orig[index].ord ^ g ^ padding_byte).chr
        if query(msg)
          plain[index] = g.chr

          puts "FOUND : %dth value = %d" % [i, g]
          puts "Plain : #{plain.inspect}"
          break
        end
      end
    end

    msg = sxor(orig[0..15], sxor(plain, "flag".ljust(16, "\x0c"))) + orig[16..-1]
    puts "FINAL : #{msg.inspect}"
    @s.write(msg + "\n")
    puts @s.readline

  end
end

s = Exploit.new
s.brute

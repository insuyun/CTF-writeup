require 'socket'
require 'openssl'

class Exploit
  KEY_SIZE = 29

  def initialize
    @s = TCPSocket.new('0.0.0.0', 4433)
    @ans = ""
  end

  def write(data)
    @s.write([data.length].pack('I') + data)
  end

  def read()
    length = @s.read(4).unpack('I')[0]
    @s.read(length)
  end

  def query(data)
    write(data)
    read()
  end

  def sxor(s1, s2)
    s1.each_byte.zip(s2.each_byte).map{|x,y| (x^y).chr}.join
  end

  def sxorl(l)
    s = "\x00" * l[0].length
    l.each {|x| s = sxor(s, x) }
    s
  end

  def dict
    ('a'..'z').to_a + ['_']
  end

  def decrypt()
    iv = @s.read(16)

    KEY_SIZE.times do
      append = 15 - (@ans.length % 16)
      prefix = ("a" * append + @ans)[-15..-1]
      block = (@ans.length / 16) * 16

      encrypted = query("a" * append)
      standard = encrypted[block..block + 15]
      new_iv = encrypted[-16..-1]

      if @ans.length >= 16
        c = @ans.length / 16 - 1
        iv = encrypted[c..c + 15]
      end

      dict.each do |ch|
        encrypted = query(sxorl([new_iv, prefix + ch, iv]))
        matching = encrypted[0..15]
        new_iv = encrypted[-16..-1]
        if matching == standard
          @ans += ch
          p @ans
          break
        end
      end

      iv = new_iv
    end
  end
end

s = Exploit.new
s.decrypt


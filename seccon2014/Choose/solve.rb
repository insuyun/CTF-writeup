require 'socket'
s = TCPSocket.new('number.quals.seccon.jp', 31337)


loop do 

min = 999999999999999999999
max = -99999999999999999999
data = s.readline
puts "[*] Data : %s" % data
data.split(",").each do |i|
  i = i.to_i
  if min > i
    min = i
  end
  if max < i
    max = i
  end
end

choose = s.read('The minimum number? '.length)
puts "[*] Q : %s" % choose
answer = ""
if choose.index("max")
  answer = "%d" % max
else
  answer = "%d" % min
end
puts "Answer : #{answer}"
s.write(answer)
end

require 'openssl'
require 'pwnbox'
require 'socket'

include Pwnbox

list = []

def get_data(p, g)
  s = TCPSocket.new('143.248.2.79', 3120)
  puts s.readline
  s.puts(p)
  puts s.readline
  s.puts(g)
  d = s.readline[18..-1].to_i
  s.close
  d
end

flags = []
primes = []
6.times do |x|
  prime = OpenSSL::BN.generate_prime(128).to_i
  flags.push((get_data(prime, 2) + get_data(prime, -2)) % prime)
  primes.push(prime)
end

p Number.i_to_s(Number.chinese_remainder_theorem(flags, primes) / 2)

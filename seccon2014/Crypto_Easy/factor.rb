require 'prime'
require 'openssl'

def factorize n
  sqrt = Math.sqrt(n).to_i
  p = 1
  loop do 
    p += 1
    break if (n % p) == 0
  end

  q = n / p

  if (q.prime? and p.prime?)
    puts "[*] Prime factor of %X : %X, %X" % [n, p, q]
  else
    puts "[*] Error : no prime factorization"
  end

  return [p,q]
end

def chinese_remainder(mods, remainders)
  max = mods.inject( :* )                            
  series = remainders.zip( mods ).map{|r,m| r.step( max, m ).to_a } 
  series.inject( :& ).first #returns nil when empty
end

def extended_gcd(a, b)
  last_remainder, remainder = a.abs, b.abs
  x, last_x, y, last_y = 0, 1, 1, 0
  while remainder != 0
    last_remainder, (quotient, remainder) = remainder, last_remainder.divmod(remainder)
    x, last_x = last_x - quotient*x, x
    y, last_y = last_y - quotient*y, y
  end
 
  return last_remainder, last_x * (a < 0 ? -1 : 1)
end
 
def invmod(e, et)
  g, x = extended_gcd(e, et)
  if g != 1
    raise 'Teh maths are broken!'
  end
  x % et
end

def solve(n, b, c)
  p,q = factorize(n)
  root = b**2 + 4 * c

  x = root.to_bn.mod_exp((p + 1)/4, p).to_i
  y = root.to_bn.mod_exp((q + 1)/4, q).to_i

#  root = chinese_remainder([p, q], [x, y])
  root = chinese_remainder([p, q], [-x, y])

  s1 = ((-b + root) * invmod(2, n)) % n
  s2 = ((-b - root) * invmod(2, n)) % n

  if ( (s1 ** 2 + s1 * b - c) % n ) == 0 and ((s2 ** 2 + s2 * b - c) % n) == 0
    puts "[*] Yeah GOT SOLUTION : #{s1.to_s(16)}, #{s2.to_s(16)}"
  else
    puts "[*] Wrong :("
  end
end

solve(0xb8ae199365,0xffeee,0x8d5051562b)
solve(0xb86e78c811, 0xfffee,  0x5ffa0ac1a2)
solve(0x7bd4071e55, 0xfefef, 0x6008ddf867)


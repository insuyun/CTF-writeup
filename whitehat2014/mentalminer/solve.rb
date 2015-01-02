# Extended Euclidean GCD algorithm
# Outputs k, u, and v such that ua + vb = k where k is the gcd of a and b
def egcd(a, b)
  u_a, v_a, u_b, v_b = [ 1, 0, 0, 1 ]
  while a != 0
    q = b / a
    a, b = [ b - q*a, a ]
    u_a, v_a, u_b, v_b = [ u_b - q*u_a, v_b - q*v_a, u_a, v_a ]
    # Each time, `u_a*a' + v_a*b' = a` and `u_b*a' + v_b*b' = b`
  end
  [ b, u_b, v_b ]
end
 
# Solve ax = 1 mod p
def invmod(a, mod)
  gcd, inverse, _ = egcd(a, mod)
  raise "No multiplicative inverse" unless gcd == 1
 
  inverse % mod
end

def solve_equation x, y
  gcd = egcd(x, 1 << 64)
  if y % gcd[0] != 0
    puts "[*] Cannot solve this problem (#{x.to_s(16)},#{y.to_s(16)})"
  end

  (gcd[1] * (y / gcd[0])) % (1 << 64)
end

def sub64 x, y
  if x > y
    x-y
  else
    x - y + (1 << 64)
  end
end

def add64 x, y
  if x == nil
    puts y.to_s(16)
  end
  (x + y) % (1 << 64)
end

def print_with_hex arr
  puts arr.pack('<Q*').unpack('H*')[0].scan(/../).map{|v| "\\x"+v}.join

end

final = [0x92434AC47C3D66EA,0x0FAF424058282E122,0x0E86454BFA4BD50B4,0x8C8448BE3158B312,0x0FE4ED38E20EB5A63,0x0E43BDB8A0634A6F6,0x56079FCB493C8CE0,0x160FA2B9CB0DAB3E,0x8239688576CAE9CA,0x268A42B656B11338]
result = [0]*10

a1 = final[1]
a1 = add64(a1, 0x4CE11B1EE3F513FC)
a1 ^= 0x56D01957AB9FE9EB
a1 = sub64(a1, 4487599898883380720)
a1 ^= 0x9992A2A71D25785
a1 = solve_equation(0x6DD08AD4F3C8FDDC, a1)
a1 = sub64(a1, 0x74E727A114B19A5D)
a1 ^= 0x6965BB0DC1636C1F
final[1] = a1

puts "a[1] : #{a1.to_s(16)}"

a4 = final[4]
a4 = add64(a4, final[0])
a4 = add64(a4, 0x5EFA2B9308194207)
a4 = solve_equation(0xF2E77A26D1437132, a4)
a4 = add64(0x7848D7779EC5E6C1, a4)
a4 = sub64(a4, 0x2338FA60FE771526)
a4 ^= 0xC971ECCE84E7CB6E
a4 = add64(a4, 6003560032679829279)
a4 = solve_equation(final[3], a4)
a4 ^= 0x90279D446A624336
a4 = add64(a4, 0x555C6166791F8A04)
a4 = sub64(a4, 0x18170B76C7179B9B)
a4 = solve_equation(0x681D14794F4EB676, a4)
a4 ^= 0xEE7B4F68490E7A60
a4 = solve_equation(0x584B94F1B1B2A51D, a4)
a4 = add64(a4, 0x5F51BFF92ED73CB2)
a4 = solve_equation(final[2], a4)
final[4] = a4
puts "a[4] : #{a4.to_s(16)}"


a3 = final[3]
a3 ^= 0xE53307CA3AAE7B93
a3 = add64(a3, 0x7DFA35E391520EF)
a3 = solve_equation(0x579D7B40C3BEC1F2, a3)
a3 = sub64(a3, 0xD450063817EC932)
a3 = solve_equation(0x8EC9FE93531E415E, a3)
a3 = add64(a3, 0x45E948E761307D1B)
a3 = solve_equation(0x8BF476F7EEA5DC58, a3)
a3 = sub64(a3, 0x226C2E2544E4D2FC)
a3 = add64(final[0], a3)
a3 = solve_equation(0x2A27B2C9ADBC0917, a3)
a3 ^= 0x91B0C9AEB3CBE061
a3 = solve_equation(0xF37BE71F85478C1B, a3)
a3 ^= 0xF2B5F319601AABEE
a3 = sub64(a3, 0x4331401D33C5D7C4)
a3 = solve_equation(0x654157940050753E, a3)
final[3] = a3
puts "a[3] : #{a3.to_s(16)}"


a5 = final[5]
a5 = sub64(a5, final[0])
a5 = add64(a5, final[2])
a5 = add64(a5, final[3])
a5 = add64(a5, 0x6896949286573B05)
a5 = sub64(a5, 0x360478A058FDA74D)
a5 ^= 0x590137045A13F8BE
a5 = add64(a5, 0x23CAC5DFBE1C9D1E)
a5 = solve_equation(0x38FCA62CD15877A, a5)
a5 ^= 0x9618013B9AA05C57
a5 = sub64(a5, 5373211695967800748)
final[5] = a5
puts "a[5] : #{a5.to_s(16)}"


a7 = final[7]
a7 = solve_equation(0x1262A653548CDE7F, a7)
a7 = sub64(a7, 2988496688772864573)
a7 ^= 1599775351030574832
a7 = add64(a7, 0x49D82C81E74CF864)
a7 = sub64(a7, 0x35A23B521FED02FC)
a7 = sub64(a7, final[6])
a7 ^= final[4] ^ 0x5B6AAE7AB0304B61
a7 = sub64(a7, 0x33B487D5497B346B)
a7 ^= final[0]
a7 = sub64(a7, final[5])
a7 ^= final[2]
a7 = solve_equation(0x706D41732AC0D8B, a7)
final[7] = a7
puts "a[7] : #{a7.to_s(16)}"


a9 = final[9]
a9 = solve_equation(2035561610200265140, a9)
a9 = solve_equation(final[8], a9)
a9 ^= 0xCBCE6B96C5F012F5
a9 = sub64(a9, final[0])
a9 = solve_equation(final[7], a9)
a9 ^= final[3] ^ 0x79FB0F4BC56FC3DA
a9 = add64(a9, final[2])
a9 = solve_equation(0xED82CC6F720D844D, a9)
a9 ^=0x363907732787E377
a9 = solve_equation(0x8F47C84F5E4086A1, a9)
a9 ^= 0x309452C680D1B6BB
a9 = add64(a9, 2256030954351004279)
a9 ^=  0xBE143EB35BD29172
a9 = sub64(a9, 3328391815942815230)
a9 ^= final[5]
a9 = solve_equation(8633655121885540594, a9)
a9 = sub64(a9, 5469157822961427337)
a9 ^= 0xD6CBA303444CE216
a9 = solve_equation(0xD50E5F1BDF27F906, a9)
a9 = sub64(a9, 9167025139151262212)
a9 = sub64(a9, final[4])
final[9] = a9
puts "a[9] : #{a9.to_s(16)}"

a0 = final[0]
a0 ^=0x3A5DF48575C1EB82
a0 = solve_equation(0x2977D611F08E59F8, a0)
a0 = sub64(a0, 0x7E7C4496BA9E2456)
final[0] = a0
puts "a[0]: #{a0.to_s(16)}"

a2 = final[2]
a2 = solve_equation(0xDC4AA7355327B1CB, a2)
a2 = sub64(a2, 0x5034A3FBF72B9DB0)
a2 = solve_equation(0x7FC6E369D16B7A9B, a2)
a2 = add64(a2, 0x6C4B7E7DA3C02373)
a2 ^=0x35D78858A05BFFDE
final[2] = a2
puts "a[2] : #{a2.to_s(16)}"

a6 = final[6]
a6 = solve_equation(0x8A2F5051F5F4AD42, a6)
a6 = add64(a6, 3149842575654986562)
a6 = solve_equation(0x2CBA7EE8E62FB917, a6)
a6 = solve_equation(final[0], a6)
a6 = sub64(a6, 3935285670026568101)
a6 ^= 0x815879E7D1960BFA
a6 = add64(a6, final[3])
a6 ^= final[2] ^ final[5]
a6 = sub64(a6, 5701715827462041548)
a6 = solve_equation(final[4], a6)
a6 = add64(a6, 4413941970159683107)
a6 = solve_equation(5320754154727686933, a6)
a6 = add64(a6, 2065949501812019541)
a6 = solve_equation(6341130792775613554, a6)
final[6] = a6
puts "a[6] : #{a6.to_s(16)}"

a = final[8]
a = sub64(a, final[1])
a ^= 0x50DAE546EB084C38
a = add64(a, 0x3BD76EA13CE160D1)
a = solve_equation(0x9C5ACE7763BAA5A7, a)
a = add64(a, 0x64E9A8EA4E8352E1)
a = solve_equation(0x5F9AA72FEBED75FD, a)
a = sub64(a, 0x338002503076DFA1)
a = sub64(a, final[2])
a = solve_equation(final[6], a)
a ^= final[3]
a = add64(a, final[0])
a ^= 0xA7E0635845D62C40
a = sub64(a, 0x3A1D1C17F189794B)
a = solve_equation(final[7], a)
a ^= final[5] ^ 0x5C21A8D2B3C90A83
a = solve_equation(0x2B2B393F6B6276ED, a)
a = sub64(a, 0x262BBC76C0C3550C)
final[8] = a
puts "a[8] : #{a.to_s(16)}"
print_with_hex final

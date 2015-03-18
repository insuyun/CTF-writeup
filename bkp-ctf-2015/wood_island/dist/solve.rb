require 'json'
require 'digest'
require 'pwnbox'
require 'socket'

include Pwnbox
include Pwnbox::Number

def sha384(m)
  Digest::SHA384.hexdigest(m).to_i(16)
end

dict = {}

File.open('sigs.txt', 'r') do |f|
  while(!f.eof?)
    obj = JSON.parse(f.readline)
    r = obj["r"]
    dict[r] = []if !dict[r]
    dict[r].push(obj)
  end
end

dict.each do |x, y|
  if y.length ==  1
    dict.delete(x)
  end
end

def solve_linear_congruence_equation(a, b, m)
  d = Pwnbox::Number.gcd(a, b)
  root = Pwnbox::Number.solve_linear_congruence_equation(a, b, m)
  return nil if !root

  res = []

  d.times do |i|
    res.push(root + i * m / d)
  end
  return res
end

def gcd(x,y)
  Pwnbox::Number.gcd(x,y)
end
def pow(a,b,c)
  Pwnbox::Number.pow(a,b,c)
end

g = 5

p = 27327395392065156535295708986786204851079528837723780510136102615658941290873291366333982291142196119880072569148310240613294525601423086385684539987530041685746722802143397156977196536022078345249162977312837555444840885304704497622243160036344118163834102383664729922544598824748665205987742128842266020644318535398158529231670365533130718559364239513376190580331938323739895791648429804489417000105677817248741446184689828512402512984453866089594767267742663452532505964888865617589849683809416805726974349474427978691740833753326962760114744967093652541808999389773346317294473742439510326811300031080582618145727

dict.each do |x, y|
  sig1, sig2 = y[0], y[1]
  s1, s2 = sig1["s"], sig2["s"]
  m1, m2 = sha384(sig1["m"]), sha384(sig2["m"])
  r = sig1["r"]
  m = p - 1

  d = Pwnbox::Number.gcd((s1 - s2), p - 1)
  root =solve_linear_congruence_equation(s1-s2, m1-m2, p-1)
  if root
    root.each do |k|
      if pow(g, k, p) == sig1["r"]
        x_l = solve_linear_congruence_equation(-r, s1 * k - m1, p - 1)

        k = rand(0..p-2)
        r = pow(g, k, p)
        go = "There is no need to be upset"
        o = {}
        o["r"] = r
        o["m"] = go

        x_l.each do |x|
          o["s"] = (sha384(go) - x * r) * Pwnbox::Number.mod_inverse(k, p - 1)
          o["s"] %= p - 1
          puts (o.to_json)
        end
      end
    end
  end
end

File.open(ARGV[0], 'rb') do |f|
  data = f.read()
  first = data.index("XXXX") + 4
  data = data[first.. -1]
  last = data.index("XXXX")

  p data[0..last - 1]
end

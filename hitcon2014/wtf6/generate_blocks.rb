def check_without_enter
	d1 = open("md5_data1", "rb").read()
	d2 = open("md5_data2", "rb").read()
	if d1.index("\n") or d2.index("\n")
		return false
	else
		return true
	end
end

PREFIX = "system('/bin/sh');"
FASTCOLL_PATH = "./fastcoll/fastcoll"
BLOCK_DIR = "./blocks/"

f = open("prefix.txt", "wb")
f.write(PREFIX)
f.close

count = 0

loop do
		system("#{FASTCOLL_PATH} prefix.txt")
		if check_without_enter
			count += 1
			d = open('md5_data1', 'rb').read()
			p d.length
			open("#{BLOCK_DIR}#{count}_0", "wb").write(d[-128..-1])
			d = open('md5_data2', 'rb').read()
			open("#{BLOCK_DIR}#{count}_1", "wb").write(d[-128..-1])

			puts "[*] #{count}th block is found!"
			
			system("mv md5_data1 prefix.txt")
		end
		break if count == 32
end

system("mv prefix.txt #{BLOCK_DIR}")

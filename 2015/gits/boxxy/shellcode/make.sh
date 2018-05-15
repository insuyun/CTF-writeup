echo "@shellcode="
nasm -f elf32 ./read.s
ruby extract.rb ./read.o

echo "@wpipe="
nasm -f elf32 ./write_pipe.s
ruby extract.rb ./write_pipe.o

echo "@rpipe="
nasm -f elf32 ./read_pipe.s
ruby extract.rb ./read_pipe.o

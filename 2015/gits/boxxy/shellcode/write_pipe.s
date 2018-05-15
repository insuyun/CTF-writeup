section     .text
global      _start

_start:
  pop eax
  pop eax
  pop eax
  pop eax ; start

  ; buf : 0xc930
  ; read
  xor eax, eax
  mov edx, eax  ; edx = 0
  mov ebx, eax  ; ebx = 0
  mov al, 3
  mov ecx, 0x804c930
  mov bl, 4
  mov dx, 0x3ff
  int 0x80

  mov edx, eax ; save result

  ; write
  xor eax, eax
  mov ebx, eax  ; ebx = 0
  mov al, 4
  mov ecx, 0x804c930
  mov bl, 7
  int 0x80

  pop eax ; end
  pop eax
  pop eax
  pop eax

section     .data

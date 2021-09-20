import sys
from typing import Any
import numpy as np

mem = np.full(65536, 0, dtype=np.uint8)
regs = np.zeros(16, dtype=np.uint8)
ip = np.uint16(0)
sp = np.uint8(0x80)
ret_stack = []
flags = np.zeros(8, dtype=np.bool_)
ZF, CF, SF, OF = 0, 1, 2, 3
IN = open('in','rb')
OUT = open('out','wb')

def concat(bits1: np.uint8, bits2: np.uint8):
    return (np.uint16(bits1) << 8) + np.uint16(bits2)

def set_flags(val1: np.uint8, val2: np.uint8):
    res = np.int8(val1)-np.int8(val2)

    flags[:4] = [res == 0, val1 < val2, res < 0, (res < 0 and np.int8(val1) > 0 and np.int8(val2) < 0) or (res > 0 and np.int8(val1) < 0 and np.int8(val2) > 0)]

def LD(rx, ry, rz):
    regs[rz] = mem[concat(regs[rx], regs[ry])]

def ST(rx, ry, rz):
    mem[concat(regs[rx], regs[ry])] = regs[rz]

def ADD(rx, ry):
    regs[rx] += regs[ry]


def SUB(rx, ry):
    regs[rx] -= regs[ry]


def MUL(rx, ry):
    regs[rx] *= regs[ry]


def DIV(rx, ry):
    regs[rx] //= regs[ry]


def MOD(rx, ry):
    regs[rx] %= regs[ry]


def SHL(rx, ry):
    regs[rx] <<= regs[ry]


def SHR(rx, ry):
    regs[rx] >>= regs[ry]


def AND(rx, ry):
    regs[rx] &= regs[ry]


def OR(rx, ry):
    regs[rx] |= regs[ry]


def XOR(rx, ry):
    regs[rx] ^= regs[ry]

def MOV(rx, ry):
    regs[rx] = regs[ry]


def ADDI(rx, imm):
    regs[rx] += imm


def SUBI(rx, imm):
    regs[rx] -= imm


def MULI(rx, imm):
    regs[rx] *= imm


def DIVI(rx, imm):
    regs[rx] //= imm


def MODI(rx, imm):
    regs[rx] %= imm


def SHLI(rx, imm):
    regs[rx] <<= imm


def SHRI(rx, imm):
    regs[rx] >>= imm


def ANDI(rx, imm):
    regs[rx] &= imm


def ORI(rx, imm):
    regs[rx] |= imm


def XORI(rx, imm):
    regs[rx] ^= imm

def MOVI(rx, imm):
    regs[rx] = imm


def CMP(rx, ry):
    set_flags(regs[rx], regs[ry])


def CMPI(rx, imm):
    set_flags(regs[rx], imm)


def JMP(addr):
    global ip
    ip = addr


def JE(addr):
    if flags[ZF]:
        JMP(addr)


def JNE(addr):
    if not flags[ZF]:
        JMP(addr)

def JL(addr):
    if flags[SF] != flags[OF]:
        JMP(addr)

def JG(addr):
    if flags[SF] == flags[OF] and not flags[ZF]:
        JMP(addr)


def CALL(addr):
    global ret_stack, ip, sp
    ret_stack.insert(0, ip)
    assert (sp >= 2), "CPU crash, too many fn calls"
    sp -= 2
    ip = addr


def RET():
    global ret_stack, ip, sp
    ip = ret_stack[0]
    ret_stack = ret_stack[1:]
    sp += 2

def INPUT(rx):
    global IN
    regs[rx] = np.frombuffer(IN.read(1),np.uint8)

def OUTPUT(rx):
    global OUT
    OUT.write(regs[rx].tobytes())

def HALT(*args):
    IN.close()
    OUT.close()
    print("Halting...")
    print(
        f"Machine State : {bytes(mem[:100])=} {regs=} {ip=} {sp=} {ret_stack=} {flags=}")
    exit(0)


def process(instr, sz: int, args):
    global ip
    ip += sz
    instr(*args)


def parse():
    instr = HALT
    sz: int = 0
    args: list = []

    op = mem[ip] >> 4

    if (0 <= op <= 1):
        sz = 2
        args = [mem[ip] % 2**4, mem[ip+1] >> 4, mem[ip+1] % 2**4]
        instr = [LD, ST][op]
    if (op == 2):
        func = mem[ip] % 2**4
        sz = 2
        args = [mem[ip+1] >> 4, mem[ip+1] % 2**4]
        if (func == 0):
            instr = ADD
        elif (func == 1):
            instr = SUB
        elif (func == 2):
            instr = MUL
        elif (func == 3):
            instr = DIV
        elif (func == 4):
            instr = MOD
        elif (func == 5):
            instr = SHL
        elif (func == 6):
            instr = SHR
        elif (func == 7):
            instr = AND
        elif (func == 8):
            instr = OR
        elif (func == 9):
            instr = XOR
        elif (func == 10):
            instr = MOV
    elif (op == 3):
        func = mem[ip] % 2**4
        sz = 3
        args = [mem[ip+1] >> 4, mem[ip+2]]
        if (func == 0):
            instr = ADDI
        elif (func == 1):
            instr = SUBI
        elif (func == 2):
            instr = MULI
        elif (func == 3):
            instr = DIVI
        elif (func == 4):
            instr = MODI
        elif (func == 5):
            instr = SHLI
        elif (func == 6):
            instr = SHRI
        elif (func == 7):
            instr = ANDI
        elif (func == 8):
            instr = ORI
        elif (func == 9):
            instr = XORI
        elif (func == 10):
            instr = MOVI
    elif (op == 4):
        sz = 2
        args = [mem[ip] % 2**4, mem[ip+1]]
        instr = CMP
    elif (op == 5):
        sz = 2
        args = [mem[ip] % 2**4, mem[ip+1]]
        instr = CMPI
    elif (6 <= op <= 10):
        sz = 3
        args = [(np.uint16(mem[ip+1]) << 8) + np.uint16(mem[ip+2])]
        instr = [JMP, JE, JNE, JL, JG][op-6]
    elif (op == 11):
        sz = 3
        args = [concat(mem[ip+1], mem[ip+2])]
        instr = CALL
    elif (op == 12):
        sz = 1
        args = []
        instr = RET
    elif (op == 13):
        sz = 1
        args = [mem[ip]%2**4]
        instr = INPUT
    elif (op == 14):
        sz = 1
        args = [mem[ip]%2**4]
        instr = OUTPUT
    elif (op == 15):
        sz = 1
        args = []
        instr = HALT

    return instr, sz, args


def load(file: str):
    with open(file, 'rb') as f:
        b = f.read()
    mem[:len(b)] = list(b)


load(sys.argv[1])
while (ip <= 0xFFFF):
    instr, sz, args = parse()
    print(
        f"Executing instruction at {ip} : {instr.__name__},{args},{mem[ip:ip+sz]}")
    process(instr, sz, args)

import numpy as np

prime = np.uint(17) # store in r15

def eea(a,b):
    l,m = a,np.uint8(1)
    r,s = b,np.uint8(0)
    while (r > 0):
        e,f = l,m
        l,m = r,s
        p = e//l
        r,s = e-p*l,f-p*m
    return (m+b)%b

def inv(x):
    if x == 0:
        return np.uint8(0)
    else:        
        return eea(np.uint8(x),prime)

def transform(x):
    return (inv(x//16)*np.uint8(16)+inv(x%16))

i = 0
s = "Enter 1-byte key :"
flag = "dc9111{h0p3_y0u_d1dn7_d0_1t_6y_h4nd}"
key = np.uint8(0x23)

inv_flag = []

rom = f'60'+hex(len(s)+len(flag)+3)[2:].zfill(4)+''.join([hex(transform(ord(i))-key)[2:].zfill(2) for i in (flag)])+''.join([hex(ord(i))[2:].zfill(2) for i in s])

#   jmp <addr>
#   ....flag
#   ....s

rom += f'3a00003a10{hex(len(flag)+3)[2:].zfill(2)}51{hex(len(s)+len(flag)+3)[2:].zfill(2)}'
#   movi r0, begu
#   movi r1, begl
#   cmpi r1, <end of s>

a = len(rom)//2+6
b = len(rom)//2+15
rom += f'90{hex(a)[2:].zfill(4)}60{hex(b)[2:].zfill(4)}'
#   jl <addr>
#   jmp <addr> 

rom += f'0012e230100160{hex(a-8)[2:].zfill(4)}'
#   ld r2, [r0,r1]
#   out r2
#   addi r1, 0x01
#   jmp <addr>

rom += f'3a00003a10033a40{hex(len(flag))[2:].zfill(2)}3a2400d53af011'
#   movi r0, flag_base_upper
#   movi r1, flag_base_lower
#   movi r4, flag_len
#   movi r2, 0x00
#   in  r5
#   movi r15, 0x11

a = len(rom)//2
b = a + 21
rom += f'2a32203100372075b0{hex(b)[2:].zfill(4)}e7302001420490{hex(a)[2:].zfill(4)}fa'
#   mov r3, r2
#   add r3, r1
#   ld r7, [r0,r3]
#   add r7, r5
#   call transform
#   out r7
#   addi r2, 0x01
#   cmp r2, r4
#   jl <addr>
#   halt

a = len(rom)//2+24
rom += f'2ab736b804b0{hex(a)[2:].zfill(4)}2ab734b7102a7c357004b0{hex(a)[2:].zfill(4)}207cc5'
# input in r7
# transform:
#   mov r11, r7
#   shri r11, 0x04
#   call compute_inv
#   mov r11, r7
#   modi r11, 0x10
#   mov r7, r12
#   shli r7, 0x04
#   call compute_inv
#   add r7, r12
#   ret

a = len(rom)//2+9
b = a+8+10
rom += f'5b00a0{hex(a)[2:].zfill(4)}3ac000c13ac0012adf3ae6005d00a0{hex(b)[2:].zfill(4)}20cf24cfce2a9b2aac2abd2ace2a89238b22d822e8219d21ae2ad92aea60{hex(b-10)[2:].zfill(4)}'
# prime in r15
# input in r11
# compute_inv:
#   cmpi r11, 0x00 - l
#   jg <addr>+(4)
#   movi r12, 0x00
#   ret

#   movi r12, 0x01 - m
#   mov r13, r15 - r
#   movi r14, 0x00 - s

#   cmpi r13, 0x00 <- jump here
#   jg <addr>+(8)
#   add r12, r15
#   mod r12, r15
#   ret

#   mov r9, r11 - e
#   mov r10, r12 - f
#   mov r11, r13
#   mov r12, r14
#   mov r8, r9  - p
#   div r8, r11
#   mul r13, r8
#   mul r14, r8
#   sub r9, r13
#   sub r10, r14
#   mov r13, r9
#   mov r14, r10
#   jmp <addr>
print(rom,len(rom))
with open('rom2.rom','wb') as f:
    f.write(bytes.fromhex(rom))
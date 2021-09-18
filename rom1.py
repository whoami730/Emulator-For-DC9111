# addi r0, 0x10
# shl r1, r1
# shr r2, r15
# addi r14, 0x1
# subi r15, 0x42 <- key = -0x42

hdr = "10 05 10 05 11 06 2f 10 e9 01 11 fa 42 "
flag = b"dc9111{3mu1ati0n_n0t_5o_6iff1cul7}"
key = 190

addr = len(hdr.strip().split())

for i in flag:
    addr += 16*14
    h, l = hex(i >> 4)[2:].zfill(2), hex(i % 2**4)[2:].zfill(2)

    # mod r4, r14 :2
    # shr r5, r15 :2
    # xori r4, <hardcodedaddr> :3
    # ori r5, <hardcodedaddr> :3
    # ld r3, [r4 r5] :2
    # xor r3, r15 :2
    # st [r4 r5], r3 :2
    # <do 14 times>
    for _ in range(14):
        x, y = hex(addr >> 8)[2:].zfill(2), hex(addr % 2**8)[2:].zfill(2)
        ins = f"04 4e 06 5f 19 45 {x} 18 55 {y} d4 53 09 3f e4 53 "
        addr += 1
        hdr += ins

    # xor r3, r3
    # addi r3, 0x6 <- higher nibble
    # mul r3, r0
    # addi r3, 0x1 <- lower nibble
    # st [r1 r2], r3
    # add r2, r14
    b = f"09 33 10 30 {h} 02 30 10 30 {l} e1 23 00 2e"

    for j in b.split():
        hdr += hex(int(j, 16) ^ key)[2:].zfill(2)
        hdr += " "

hdr += "f0"

with open('rom1.rom', 'wb') as f:
    f.write(bytes.fromhex(hdr))

import subprocess

instrs = ['B00007E100FAF5C5']
for i in instrs:
    with open('test.rom', 'wb') as f:
        f.write(bytes.fromhex(i))
    p = subprocess.run(["python3", "emu.py", "test.rom"], capture_output=True)
    print(p.stdout)

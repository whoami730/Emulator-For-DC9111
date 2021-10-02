# DC-v0.69 system

We're given a manual for an old system and several `rom` files. We realise that we have been asked to build an emulator for the mentioned system supporting the CPU, the memory, serial I/O and all the mentioned instructions as well!

We observe that the given system consists of 16 general purpose registers, a 16-bit `IP` and two other 8-bit registers `SP` and `FLAGS`; the memory addresses range from 0 to 65535, and we have an additional data structure called `ret-stack` for holding return addresses.

The first challenge `ez` hints that only arithmetic and memory operations are required initially. 

Since the instructions are encoded in "Big-Endian" format; the current byte allows us to find out the instruction to be executed simply by picking the first 4 bits of the instruction, denoting the op-code. Based on the op-code, the arguments to the operation as well as the size of the instruction can be obtained. 

One thing we need to be careful about is the fact that since registers are 8-bits, arithmetic operations need to be carefully performed keeping in mind the overflows that may happen. If one chooses to use `python` as the language to create their own emulator, an easy way out is to use `numpy.uint8` or `Z3.BitVecVal` for performing the arithmetic without having to worry about the overflows ourselves. In `C/C++`, simply using `uint8` would do.

There are a few steps that we will need to follow to ensure that instructions are correctly executed -  
1. The instruction needs to be parsed to obtain the op-code + arguments; invalid instruction should default to the `HALT` instruction.
2. After parsing the instruction, we need to update the IP as well as process the instruction
3. Certain instructions have some side-effects such as IN/OUT,LD/ST,HALT or CMP/CMPI. These side-effects need to be taken care of as well. (Not in the first `ez` challenge!)

## Parsing the instructions

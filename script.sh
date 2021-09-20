#!/bin/bash

touch in
echo -en '\x23' > in
python3 emu.py $1

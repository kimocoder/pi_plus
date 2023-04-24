#!/usr/bin/env python2

import os
import re
import sys

try:
   kernel_image = sys.argv[1]
except:
   kernel_image = ""

if not kernel_image:
   print("usage : imagetool-uncompressed.py <kernel image>");
   sys.exit(0)

re_line = re.compile(r"0x(?P<value>[0-9a-f]{8})")

mem = [0 for _ in range(32768)]

def load_to_mem(name, addr):
   with open(name) as f:
      for l in f:
         if m := re_line.match(l):
            value = int(m.group("value"), 16)

            for i in range(4):
               mem[addr] = int(value >> i * 8 & 0xff)
               addr += 1

load_to_mem("boot-uncompressed.txt", 0x00000000)
load_to_mem("args-uncompressed.txt", 0x00000100)

with open("first32k.bin", "wb") as f:
   for m in mem:
      f.write(chr(m))

os.system(f"cat first32k.bin {kernel_image} > kernel.img")

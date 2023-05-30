from ptrlib import ELF
import sys

kernel = ELF("tmp/vmlinux")
print(hex(next(kernel.search(sys.argv[1] + "\0"))))
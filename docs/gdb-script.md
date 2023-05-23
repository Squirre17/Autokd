templete
use `cat /sys/module/babydriver/sections/.text ` or `cat /proc/kallsyms | tail` or `cat /proc/modules ` to get driver base

add these in gdbscript(must set PYTHONPATH in advance(in akd script))
```shell
gef-remote --qemu-user --qemu-binary tmp/vmlinux localhost 1234
add-symbol-file notebook.ko 0xffffffffc0000000
so plugins/bp.py
bda set 0xffffffffc0000000
bka set 0xffffffff81000000
```
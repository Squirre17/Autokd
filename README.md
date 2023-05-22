automate kernel deploy

# procedure

~~pull a docker with built-in qemu and pwn environment, compile kernel locally and transfer bzImage into docker.~~

A full dockerized project now avaiable in [like-dbg](https://github.com/0xricksanchez/like-dbg). So I don't use docker now.

idea from ref here : https://eternalsakura13.com/2020/07/11/kernel_qemu/#more


# TODO
## ctf
- provide a vmlinux and initrd.cpio

## compile
- gcc argument configurable
- musl support

# Tips
- If want unpack cpio again. just remove the `resource/initrd.modified.cpio`
- bzImage for qemu launch, vmlinux for gdb debug
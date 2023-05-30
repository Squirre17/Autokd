automate kernel deploy

# procedure

~~pull a docker with built-in qemu and pwn environment, compile kernel locally and transfer bzImage into docker.~~

A full dockerized project now avaiable in [like-dbg](https://github.com/0xricksanchez/like-dbg). So I don't use docker now.

idea from ref here : https://eternalsakura13.com/2020/07/11/kernel_qemu/#more


# TODO
## compile
- gcc argument configurable
- musl support

# Tips
- If want unpack cpio again. just remove the `resource/initrd.modified.cpio`
- bzImage for qemu launch, vmlinux for gdb debug
- `use-custom-qemu-script` option allow user to use costom script(e.g. ctf provided) to launch qemu, which location is fixed at `./qemu-custom.sh`
fill any thing in `config/user.json`
```json
{
    "kernel-version" : "5.10",
    "initrd-is-root-used" : false,
    "confirmation-before-running" : true,
    "nproc" : 2,
    "qemu-option" : {
        "semp" : false,
        "samp" : false,
        "kaslr" : false,
        "kpti" : false,
        "cores" : 1,
        "threads" : 1
    },
    "ctf" : {
        "enable-ctf-mode" : false,
        "bzimage-path" : "/tmp/akd/kernel-challenge/knote/bzImage",
        "use-custom-qemu-script" : false
    }
}
```

# usage
```shell
chmod +x ./akd
./akd run
# or
./akd ctf
# or skip confirmation
./akd ctf skip
```

scripts
```shell
$ py scripts/string-search-in-kernel.py /sbin/modprobe
0xffffffff8225d2e0
```

gcc options
```json
    "gcc" : {
        "compile-option" : "-D_FILE_OFFSET_BITS=64",
        "lib-dep" : "-lfuse"
    }
```

highlight address 
```c
```c
ok("Hello Autokd" cRED " 0x%lx" cRST, (u64)main);
```
```
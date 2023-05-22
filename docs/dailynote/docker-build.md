
```shell

docker run -it --name=autokd --cap-add=SYS_PTRACE -p 1234:1234 ubuntu:20.04 /bin/bash
# or
docker run -id --name=autokd --cap-add=SYS_PTRACE -p 1234:1234 ubuntu:20.04 /bin/bash # background run


# docker 
# sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list
apt-get update && apt-get -y dist-upgrade

alias agi="/bin/apt-get install -y"
agi vim gdb gdbserver wget make gcc flex bison bc git cpio ninja-build pkg-config automake libtool
agi libncurses-dev openssl libssl-dev dkms libelf-dev libudev-dev libpci-dev libiberty-dev autoconf libglib2.0-dev
agi libpixman-1-dev python python3 libglib2.0-dev libpixman-1-dev

export http_proxy=http://192.168.18.1:7890
export https_proxy=$http_proxy 
wget https://download.qemu.org/qemu-6.2.0.tar.xz
mkdir build && cd build  # 在下载目录新建文件夹build（这是必须的，因为configure命令必须在build文件夹下执行）
# 以下均在/build目录下
../configure --target-list=x86_64-softmmu,arm-softmmu
make -j2 && make install

```
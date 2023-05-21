#!/bin/bash
path=$PWD
set -eu
RED="\033[31m"
BLUE="\033[34m"
GREEN="\033[32m"
DFT="\033[0m" # default
if [ -d $path/rootfs ]; then
	echo -e "[${BLUE}*${DFT}] rm rootfs/*"
	rm -rf $path/rootfs/*
fi

if [ -d $path/etc ]; then
	echo -e "[${BLUE}*${DFT}] rm etc/"
	rm -rf $path/etc
fi
if [ -f $path/vmlinux ]; then
	echo -e "[${BLUE}*${DFT}] rm vmlinux"
	rm -rf $path/vmlinux
fi
if [ -f $path/initrd.modified.cpio ]; then
	echo -e "[${BLUE}*${DFT}] rm initrd.modified.cpio"
	rm -rf $path/initrd.modified.cpio
fi
if [ -f $path/initrd.cpio ]; then
	echo -e "[${BLUE}*${DFT}] rm initrd.cpio"
	rm -rf $path/initrd.cpio
fi
echo -e "[${GREEN}+${DFT}] clean.sh done"
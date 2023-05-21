#!/bin/bash
# -e if error happen , exit immediately
# -u if unassigned argu exist , exit immediately
set -eu
path=$PWD # path in the time executing
RED="\033[31m"
BLUE="\033[34m"
GREEN="\033[32m"
AMARANTH='\033[35m'
DFT="\033[0m" # default
if [ ! -f "$path/initrd.cpio" ]; then
	echo -e "[${RED}!${DFT}] Error: $path/initrd.cpio not found.(Maybe need rename)"
	exit 1
fi
if [ ! -d "$path/rootfs" ]; then
	echo -e "[${RED}!${DFT}] Error: $path/rootfs directory isn't found"
	exit 1
fi
# if [ [ $# -ne 1 ] -o [ [ $1 -ne "zip" ] -a [ $1 -ne "unzip" ] ] ]; then
if [[ $# -ne 1 ]]; then
	echo -e "[${RED}!${DFT}] Error: zip / unzip argument needed"
	exit 1
fi

cd $path/rootfs

if [ $1 == "zip" ]; then
	echo -e "[${BLUE}*${DFT}] Pack back to initrd.modified.cpio..."
	echo -e "[${BLUE}*${DFT}] if img is root use, then modify here"
	if [ `whoami` == "root" ]; then
		echo -e "[${AMARANTH}#${DFT}] root branch"
		find . -print0 | cpio -o --null --format=newc --owner root > ../initrd.modified.cpio
	else
		echo -e "[${AMARANTH}#${DFT}] non-root branch"
		find . -print0 | cpio -o --null --format=newc > ../initrd.modified.cpio
	fi
	chmod +x ../initrd.modified.cpio
elif [ $1 == "unzip" ]; then
	if [ ! -s $path/rootfs/flag ]; then # -s => exist and not empty
		echo -e "[${BLUE}*${DFT}] Unzip initrd.cpio file..."
		cpio -idmv < ../initrd.cpio
	fi
else
	echo -e "[${RED}!${DFT}] Error: unknow argument ,zip / unzip needed"
	exit 1
fi
echo -e "[${GREEN}+${DFT}] cpio.sh done"
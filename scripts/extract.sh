#!/bin/bash
path=$PWD
set -eu
RED="\033[31m"
BLUE="\033[34m"
GREEN="\033[32m"
DFT="\033[0m" # default
if [ ! -f $path/bzImage ]; then
	echo -e "[${RED}!${DFT}] Error: $path/bzImage not exist"
	exit 1
fi

/usr/src/linux-headers-$(uname -r)/scripts/extract-vmlinux bzImage > vmlinux
echo -e "[${GREEN}+${DFT}] extract.sh done"
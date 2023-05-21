#!/bin/bash
set -eu
RED="\033[31m"
BLUE="\033[34m"
GREEN="\033[32m"
DFT="\033[0m" # default
if [ ! -f "./initrd.cpio" ];
then
	cp *.cpio initrd.cpio;
fi
echo -e "[${GREEN}+${DFT}] rename.sh done"
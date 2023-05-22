#!/bin/bash
set -eu
RED="\033[31m"
BLUE="\033[34m"
GREEN="\033[32m"
DFT="\033[0m" # default

ERR="${RED}[!]${DFT}"
NOTE="${BLUE}[*]${DFT}"
INFO="${GREEN}[+]${DFT}"

if [ "$#" -ne 1 ]; then
  echo -e "${ERR} Invalid argument. Usage: $0 <bzImage_path>"
  exit 1
fi

bzimg_path="$1"

if [ ! -f "$bzimg_path" ]; then
  echo -e "${ERR} Error: $bzimg_path does not exist or is not a file."
  exit 1
elif [ "$(basename "$bzimg_path")" != "bzImage" ]; then
  echo -e "${ERR} Error: $bzimg_path name is not a bzImage."
  exit 1
fi

mkdir -p tmp
/usr/src/linux-headers-$(uname -r)/scripts/extract-vmlinux "$bzimg_path" > tmp/vmlinux
echo -e "${INFO} extract.sh done"
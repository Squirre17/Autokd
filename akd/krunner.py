import os
import urllib
import urllib.error
import urllib.request
import requests
import tarfile
import shutil
import akd.utils.printer as printer
import subprocess as sp

from tqdm             import (tqdm)
from typing           import (Type)
from pathlib          import (Path)
from typing           import (List)
from loguru           import (logger)
from akd.utils.dynbar import (Dynbar)
from akd.config       import (config)

class Krunner:

    def __init__(self) -> None:
        pass

    def make_run_script(self) -> None:
        '''shell
        qemu-system-x86_64 \
            -m 256M \
            -kernel ./bzImage \
            -initrd ./initrd.modified.cpio \
            -append "console=ttyS0 oops=panic panic=1 quiet nokaslr" \
            -no-reboot \
            -smp cores=2,threads=2 \
            -cpu kvm64,+smep,+smap \
            -monitor /dev/null \
            -nographic \
            -net nic,model=virtio \
            -net user \
            -device e1000 \
            -monitor /dev/null
        '''

        # temp
        cmd = '''
        qemu-system-x86_64
            -m 256M
            -kernel {bzimage_path}
            -initrd {initrd_path}
            -append "console=ttyS0 oops=panic panic=1 quiet nokaslr"
            -no-reboot
            -cpu qemu64
            -nographic
            -net nic,model=virtio
            -net user
            -monitor /dev/null
        '''.format(
            bzimage_path = config.bzimage_path,
            initrd_path  = TODO
        )
        ...
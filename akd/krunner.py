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
        config.qemu_script_path = config.scripts_dir_path / "qemu-run.sh"
        ...

    def make_run_script(self) -> Type["Krunner"]:
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

        assert config.bzimage_path.exists()
        assert config.initrd_path.exists()

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
            -s
        '''.format(
            bzimage_path = config.bzimage_path,
            initrd_path  = config.initrd_path
        )

        if config.qemu_script_path.exists():
            printer.warn("TEMP : not change if exist")
            return self

        with open(config.qemu_script_path,  "+w") as f:
            f.writelines(cmd.splitlines())

        os.chmod(config.qemu_script_path, 0o755)

        return self
    
    def run(self) -> None:

        assert config.qemu_script_path.exists()
        "todo : maybe this part let user to do more batter"
        
        sp.run(["bash", config.qemu_script_path.absolute()], shell=True)

krunner = Krunner()
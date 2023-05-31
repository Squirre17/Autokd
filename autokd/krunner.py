import os
import urllib
import shutil
import tarfile
import requests
import urllib.error
import urllib.request

import subprocess           as sp
import autokd.utils.printer as printer

from tqdm                import (tqdm)
from typing              import (Type)
from pathlib             import (Path)
from typing              import (List)
from loguru              import (logger)
from autokd.utils.dynbar import (Dynbar)
from autokd.config       import (config)

def path_must_exist(p : Path):
    if not p.exists():
        printer.fatal(
            "{} not found, abort".format(p.absolute())
        )

class Krunner:

    def __init__(self) -> None:

        assert config.qemu_script_path is not None
        path_must_exist(config.exp_src_path)

        
        self.cmd = None
        

    def make_run_script(self) -> Type["Krunner"]:
        '''example
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
            -s
        '''

        path_must_exist(config.bziamge_path)
        path_must_exist(config.modified_initrd_path)

        # generate cpu_protect str
        cpu_protect = ""
        if config.qemuopts.smep:
            cpu_protect += ",+smep"
        if config.qemuopts.smap:
            cpu_protect += ",+smap"

        # generate ct_num str
        ct_num = "cores={},threads={}".format(
            config.qemuopts.cores, config.qemuopts.threads
        )

        # generate kaslr str
        kaslr = "kaslr" if config.qemuopts.kaslr else "nokaslr"

        #generate pti str
        kpti  = "pti" if config.qemuopts.kpti else "nopti"

        # TODO: -monitor /dev/null

        # temp
        self.cmd = '''qemu-system-x86_64
            -m 128M
            -kernel {bzimage_path}
            -initrd {modified_initrd_path}
            -append "console=ttyS0 loglevel=3 oops=panic panic=-1 {kaslr} {kpti}"
            -no-reboot
            -cpu qemu64{cpu_protect}
            -smp {ct_num}
            -nographic
            -net nic,model=virtio
            -net user
            -s'''.format(
                bzimage_path          = config.bziamge_path,
                modified_initrd_path  = config.modified_initrd_path,
                cpu_protect           = cpu_protect,
                ct_num                = ct_num,
                kaslr                 = kaslr,
                kpti                  = kpti
        )

        # overhead is very low so dont need to 
        # if config.qemu_script_path.exists():
        #     printer.warn("TEMP : not change if exist")
        #     return self

        # wait late write to qemu script when qemu-custom is true

        return self
        
    def run(self) -> None:

        assert config.qemu_script_path is not None
        "todo : maybe this part let user to do more batter"

        if not config.ctfopts.use_custom_qemu_script:# only writeback when not custom qemu script enabled        
            with open(config.qemu_script_path,  "+w") as f:
                f.write("  \\\n".join(self.cmd.splitlines()))

            os.chmod(config.qemu_script_path, 0o755)
        
        if config.msicopts.need_confirm:
            printer.note("run qemu now [Y/n] ", not_line_break=True)# tmp
            opt = input("")
            if opt == "n":
                printer.fatal("exit")
            
        assert os.access(config.qemu_script_path, os.X_OK)
        sp.run([config.qemu_script_path.absolute()], shell=True)

krunner = Krunner()
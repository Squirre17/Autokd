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

class Krunner:

    def __init__(self) -> None:
        config.qemu_script_path = config.scripts_dir_path / "qemu-run.sh"
        config.exp_src_path     = Path.cwd() / "exp.c"
        if not config.exp_src_path.exists():
            printer.fatal("{} not found, abort".format(config.exp_src_path.absolute()))
        

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
            -s
        '''

        assert config.bzimage_path.exists()
        assert config.modified_initrd_path.exists()

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

        # temp
        cmd = '''qemu-system-x86_64
            -m 256M
            -kernel {bzimage_path}
            -initrd {modified_initrd_path}
            -append "console=ttyS0 oops=panic panic=1 quiet {kaslr}"
            -no-reboot
            -cpu qemu64{cpu_protect}
            -smp {ct_num}
            -nographic
            -net nic,model=virtio
            -net user
            -monitor /dev/null
            -s'''.format(
                bzimage_path          = config.bzimage_path,
                modified_initrd_path  = config.modified_initrd_path,
                cpu_protect           = cpu_protect,
                ct_num                = ct_num,
                kaslr                 = kaslr
        )

        # overhead is very low so dont need to 
        # if config.qemu_script_path.exists():
        #     printer.warn("TEMP : not change if exist")
        #     return self

        with open(config.qemu_script_path,  "+w") as f:
            f.write("  \\\n".join(cmd.splitlines()))

        os.chmod(config.qemu_script_path, 0o755)

        return self

    def compile_exp(self) -> Type["Krunner"]:

        assert config.exp_src_path.exists()

        exp_output_path = config.unpacked_fs_dir_path / "exp"
        cmd = "gcc -g -o {out} {src} --static -lpthread".format(
            out = exp_output_path.absolute(),
            src = config.exp_src_path.absolute()
        ) # TODO: maybe provide by user?

        printer.info("conpiling the exp...")
        result = sp.run(cmd, shell=True) # TODO: configuable for capture output , capture_output=True)
        if result.returncode != 0:
            printer.fatal(f"compile failed with result {result}")

        # TODO: symbol recover
        return self

        
    def run(self) -> None:

        assert config.qemu_script_path.exists()
        "todo : maybe this part let user to do more batter"
        
        if config.msicopts.need_confirm:
            printer.note("run qemu now [Y/n] ", not_line_break=True)# tmp
            opt = input("")
            if opt == "n":
                printer.fatal("exit")
            
        
        assert os.access(config.qemu_script_path, os.X_OK)
        sp.run([config.qemu_script_path.absolute()], shell=True)

krunner = Krunner()
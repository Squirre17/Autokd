'''
deal with initrd.cpio
'''

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


class Initrd:
    def __init__(self) -> None:
        if not config.resource_dir_path.exists():
            config.resource_dir_path.mkdir()

        config.modified_initrd_path = config.resource_dir_path /  "initrd.modified.cpio";
        config.initrd_path          = config.resource_dir_path /  "initrd.cpio";

        if config.initrd_is_root_used:
            self.packcmd = "find . -print0 |" \
                           " cpio -o --null --format=newc --owner root > " \
                           "{}".format(config.modified_initrd_path.absolute())
        else:
            self.packcmd = "find . -print0 |" \
                           " cpio -o --null --format=newc > " \
                           "{}".format(config.modified_initrd_path.absolute())

        self.unpackcmd = "cpio -idmv < {}".format(
            config.initrd_path.absolute()
        )

    def pack(self) -> None:

        if not config.initrd_path.exists():
            printer.fatal("initrd not exist, missing key file")

        if config.initrd_path.name != "initrd.cpio":
            printer.fatal(
                f"current need target initrd called after `initrd.cpio`, " \
                 "but {config.initrd_path.name} given"
            )
        
        printer.info("packing initrd.cpio...")
        
        cur_dir = Path.cwd()
        os.chdir(config.unpacked_fs_dir_path)
        sp.run(self.packcmd, shell=True)
        sp.run("chmod +x {}".format(config.modified_initrd_path.absolute()), shell=True)
        os.chdir(cur_dir)

        return

    def unpack(self) -> Type["Initrd"]:
        '''
        only do once
        '''

        if config.modified_initrd_path.exists():
            printer.note("initrd is unpacked already, skip this stage")
            return self

        if not config.unpacked_fs_dir_path.exists():
            config.unpacked_fs_dir_path.mkdir()

        cur_dir = Path.cwd()
        os.chdir(config.unpacked_fs_dir_path)
        sp.run(self.unpackcmd, shell=True)
        os.chdir(cur_dir)

        return self

    def compile_exp(self) -> Type["Initrd"]:

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
        
initrd = Initrd()
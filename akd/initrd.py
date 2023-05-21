'''
deal with initrd.cpio
'''

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


class Initrd:
    def __init__(self) -> None:
        config.modified_initrd_path = config.resouce_path /  "initrd.modified.cpio";

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
        os.chdir(config.resouce_path)
        logger.debug(self.packcmd)
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
        logger.debug(self.unpackcmd)
        sp.run(self.unpackcmd, shell=True)
        os.chdir(cur_dir)

        return self
        
initrd = Initrd()
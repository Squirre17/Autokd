'''
extract vmlinux from bzImage
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


class Extractor:

    def __init__(self) -> None:
        pass

    def extract_vmlinux(self) -> Type["Extractor"]:

        assert config.bziamge_path.exists()
        assert config.script_extract_path.exists()

        if config.vmlinux_path.exists():
            printer.note(
                "{} already exist, skip extract".format(
                    config.vmlinux_path.absolute()
                )
            )
            return self

        if not os.access(config.script_extract_path, os.X_OK):
            printer.fatal(
                f"{config.script_extract_path.absolute()} not executable"
            )

        printer.info("extracting vmlinux from bzimage")
        cmd = "{extr} {bzimg}".format(
            extr  = config.script_extract_path.absolute(),
            bzimg = config.bziamge_path
        )

        sp.run(cmd, shell=True)

        assert config.vmlinux_path.exists()


extractor = Extractor()
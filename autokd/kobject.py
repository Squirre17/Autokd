'''
base class for all k-module
'''


import os
import urllib
import urllib.error
import urllib.request
import requests
import tarfile
import shutil
import autokd.utils.printer as printer
import subprocess as sp

from tqdm             import (tqdm)
from typing           import (Type)
from pathlib          import (Path)
from typing           import (List)
from loguru           import (logger)
from autokd.utils.dynbar import (Dynbar)
from autokd.config       import (config)


class Kobj:
    def __init__(self) -> None:
        self.target_name        : str  = "linux-" + config.kernel_version + ".tar.gz"                      # full path
        self.target_path        : Path = self.DOWNLOAD_PATH / self.target_name
        self.download_url       : str  = "{url}/{target}".format(
            url = config.linux_url,
            target = self.target_name
        )
        self.kernel_preroot_dir : Path = Path.cwd() / "kernel-root" # not real root
        self.unpacked_dir_name  : str  = self.target_name.replace(".tar.gz", "") # convert linux-2.6.0.tar.gz => linux-2.6.0
        self.kernel_root_dir    : Path = self.kernel_preroot_dir / self.unpacked_dir_name
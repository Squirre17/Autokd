import os
import urllib
import urllib.error
import urllib.request
import requests
import akd.utils.printer as printer

from typing           import (Type)
from pathlib          import (Path)
from typing           import (List)
from akd.utils.dynbar import (Dynbar)
from akd.config       import (config)

class Checker:
    PROXY_CHECK_LIST : List[str] = [
        "http_proxy",
        "https_proxy",
    ]

    def __init__(self) -> None:
        pass

    def proxy(self) -> None:
        for checkee in self.PROXY_CHECK_LIST:
            if checkee in os.environ:
                printer.info("{} have set with {}".format(checkee, os.environ[checkee]))
            else:
                printer.warn("{} not set".format(checkee))
    def root(self) -> None:
        '''
        check whether in correct root directory to run this script
        '''
        raise NotImplementedError
checker = Checker()
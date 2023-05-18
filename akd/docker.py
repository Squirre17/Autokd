import os
import akd.utils.printer as printer

from typing     import (List)
from akd.config import (config)

class Docker:
    '''
    be responsible to docker pull, shared volume, docker network 

    '''
    PROXY_CHECK_LIST : List[str] = [
        "http_proxy",
        "https_proxy",
    ]
    
    def __init__(self) -> None:
        ...

    def proxy_check(self) -> None:
        for checkee in self.PROXY_CHECK_LIST:
            if checkee in os.environ:
                printer.info("{} have set with {}".format(checkee, os.environ[checkee]))

    def pull(self) -> None:
        url = config.docker_url
        cmd = f"docker pull {url}" # note here not need privilege
        os.system(cmd)
    


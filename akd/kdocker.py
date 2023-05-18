import os
import docker
import docker.errors
import akd.utils.printer as printer

from docker.models.images import (Image)
from akd.config           import (config)
from docker               import (DockerClient)
from typing               import (List, Optional)

class Docker:
    '''
    be responsible to docker pull, shared volume, docker network 

    '''
    PROXY_CHECK_LIST : List[str] = [
        "http_proxy",
        "https_proxy",
    ]

    def __init__(self) -> None:
        self.client   : DockerClient = docker.from_env()
        self.img_name : str          = config.image_name # image name with tag
        ...

    def proxy_check(self) -> None:
        for checkee in self.PROXY_CHECK_LIST:
            if checkee in os.environ:
                printer.info("{} have set with {}".format(checkee, os.environ[checkee]))

    def find_image(self, tag = None) -> Optional[Image]:
        '''
        find a image locally
        '''
        if not tag:
            tag = self.img_name

        try:
            return self.client.images.get(tag)
        except docker.errors.ImageNotFound:
            return None
        
    def pull(self) -> None:

        if self.find_image(): # local image exist
            return

        url = config.docker_url
        cmd = f"docker pull {url}" # note here not need privilege
        os.system(cmd)
    


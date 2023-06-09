import os
import docker
import docker.errors
import subprocess as sp
import autokd.utils.printer as printer

from docker.models.images import (Image)
from autokd.config           import (config)
from docker               import (DockerClient)
from typing               import (List, Optional, Type)

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

    def __proxy_check(self) -> None:
        for checkee in self.PROXY_CHECK_LIST:
            if checkee in os.environ:
                printer.info("{} have set with {}".format(checkee, os.environ[checkee]))
            else:
                printer.warn("{} not set".format(checkee))

    def __find_image(self, tag = None) -> Optional[Image]:
        '''
        find a image locally
        '''
        if not tag:
            tag = self.img_name

        try:
            return self.client.images.get(tag)
        except docker.errors.ImageNotFound:
            return None
        
    def pull(self) -> Type["Docker"]:

        if self.__find_image(): # local image exist
            printer.info("found local image, use it")
            return
        
        printer.info("not found local image, start to pull")

        url = config.docker_url
        cmd = f"docker pull {url}" # note here not need privilege
        sp.run(cmd.split()) # subprocess.run will block current thread
        return self
    
    def setup_ssh(self) -> Type["Docker"]:
        raise NotImplementedError
        return self


kdocker = Docker()
    


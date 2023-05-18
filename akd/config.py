import os
import json
import akd.utils.printer as printer

from pathlib import Path
from loguru  import logger

class Config:
    '''
    parse user/sys config file (current use .json).
    '''
    SYS_CONF  = Path.cwd() / "config" / "sys.json"
    USER_CONF = Path.cwd() / "config" / "user.json"

    def __init__(self) -> None:

        self.__docker_url : str = ""
        self.__linux_url  : str = ""
        pass

    def parse(self) -> None:
        try:
            with open(self.SYS_CONF) as sysf:
                conf = json.load(sysf);
                self.__docker_url      : str = conf["docker-url"]  # e.g : squirre17/dirtypipe:1.0
                self.__linux_url       : str = conf["liunx-url"]    
                self.__image_name      : str = self.__docker_url.split("/")[1] # e.g. squirre17/dirtypipe:1.0 => dirtypipe:1.0 
                self.__kernel_src_path : str = Path.cwd() / "kernel-src"
                logger.dbg(self.__docker_url);

        except FileNotFoundError:
            printer.fatal("{} not found".format(os.path.abspath(self.SYS_CONF)))
        
        try:# TODO:
            with open(self.USER_CONF) as userf:

                pass
        except Exception:
            raise Exception
    
    @property
    def docker_url(self) -> str:
        '''
        e.g. : squirre17/dirtypipe:1.0
        '''
        return self.__docker_url

    @property
    def image_name(self) -> str:
        '''
        e.g. : "my-image:latest"
        '''
        return self.__image_name
    
    @property
    def kernel_src_path(self) -> str:
        return self.__kernel_src_path

config = Config()
config.parse()


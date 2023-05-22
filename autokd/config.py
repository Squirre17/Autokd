import os
import json
import functools

import autokd.utils.printer as printer

from pathlib import (Path)
from loguru  import (logger)
from typing  import (Callable, Any)

def return_no_none(f : Callable) -> Callable:
    @functools.wraps(f)
    def wrapper(*args, **kwargs) -> Any:
        ret = f(*args, **kwargs)
        if ret is None:
            printer.err(f"{f} return a none")
            raise RuntimeError
        return ret
    return wrapper

class Config:
    '''
    parse user/sys config file (current use .json).
    '''
    SYS_CONF  = Path.cwd() / "config" / "sys.json"
    USER_CONF = Path.cwd() / "config" / "user.json"

    def __init__(self) -> None:

        # url path
        self.docker_url             : str  = None
        self.linux_url              : str  = None
        self.kernel_version         : str  = None
        self.target_name            : str  = None # merely name
        self.target_path            : Path = None # full path
        self.download_url           : str  = None
        self.kernel_preroot_dir     : Path = None # not real root
        self.unpacked_dir_name      : str  = None # e.g. linux-2.6.0
        self.kernel_root_dir        : Path = None #
        self.bzimage_path           : Path = None
        self.initrd_path            : Path = None
        self.modified_initrd_path   : Path = None
        self.initrd_is_root_used    : bool = False

        # dir path
        self.resource_dir_path      : Path = Path.cwd() / "resource"
        self.scripts_dir_path       : Path = Path.cwd() / "scripts"
        self.unpacked_fs_dir_path   : Path = Path.cwd() / "fsroot"
        # qemu
        self.qemu_script_path       : Path = None
        pass

    def parse(self) -> None:
        try:
            with open(self.SYS_CONF) as sysf:
                conf = json.load(sysf)
                self.docker_url      : str = conf["docker-url"]  # e.g : squirre17/dirtypipe:1.0
                self.linux_url       : str = conf["linux-url"]    
                self.image_name      : str = self.docker_url.split("/")[1] # e.g. squirre17/dirtypipe:1.0 => dirtypipe:1.0 
                self.kernel_src_path : str = Path.cwd() / "kernel-src"
                logger.debug(self.docker_url);

        except FileNotFoundError:
            printer.fatal("{} not found".format(os.path.abspath(self.SYS_CONF)))
        
        try:# TODO:
            with open(self.USER_CONF) as userf:
                conf = json.load(userf)
                self.kernel_version : str = conf["kernel-version"] # e.g. v5.10-rc1
                
                is_root_use : str = conf["initrd-is-root-used"] # TODO optimize here for empty key judge
                if is_root_use.lower() == "true":
                    self.initrd_is_root_used = True
                elif is_root_use.lower() == "false":
                    self.initrd_is_root_used = False
                else:
                    raise KeyError # TODO

                pass
        except Exception:
            raise Exception


config = Config()
config.parse()

    # @property
    # @return_no_none
    # def docker_url(self) -> str:
    #     '''
    #     e.g. : squirre17/dirtypipe:1.0
    #     '''
    #     return self.__docker_url
    
    # @docker_url.setter
    # def docker_url(self, url : str) -> None:
    #     self.__docker_url = url

    # @property
    # @return_no_none
    # def image_name(self) -> str:
    #     '''
    #     e.g. : "my-image:latest"
    #     '''
    #     return self.__image_name
    
    # @image_name.setter
    # def image_name(self, name : str) -> None:
    #     self.__image_name = name

    # @property
    # @return_no_none
    # def kernel_src_path(self) -> str:
    #     return self.__kernel_src_path
    
    # @kernel_src_path.setattr
    # def kernel_src_path(self, path) -> None:
    #     self.__kernel_src_path = path

    # @property
    # @return_no_none
    # def kernel_version(self) -> str:
    #     return self.__kernel_version

    # @kernel_version.setter
    # def kernel_version(self, v) -> None:
    #     self.__kernel_version = v;
    
    # @property
    # @return_no_none
    # def linux_url(self) -> str:
    #     return self.__linux_url
    
    # @linux_url.setter
    # def linux_url(self, url) -> str:
    #     self.__linux_url = url

    



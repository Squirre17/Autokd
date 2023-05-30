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

def path_must_exist(p : Path): # temp
    if not p.exists():
        printer.fatal(
            "{} not found, abort".format(p.absolute())
        )

class QemuConfig:
    def __init__(self, conf) -> None:
        self.smep     : bool = conf["qemu-options"]["smep"]
        self.smap     : bool = conf["qemu-options"]["smap"]
        self.kaslr    : bool = conf["qemu-options"]["kaslr"]
        self.kpti     : bool = conf["qemu-options"]["kpti"]
        self.cores    : int  = conf["qemu-options"]["cores"]
        self.threads  : int  = conf["qemu-options"]["threads"]

        pass

class MsicConfig:
    def __init__(self, conf) -> None:
        self.need_confirm : bool = conf["confirmation-before-running"]
        
class CtfConfig:
    def __init__(self, conf) -> None:
        self.enabled : bool = conf["ctf"]["enable-ctf-mode"]
        # enable ctf mode will default to use provided bzimage path
        printer.note("use ctf provided bzimage")
        self.bzimage_path = Path(conf["ctf"]["bzimage-path"])
        path_must_exist(self.bzimage_path)
        
        self.use_custom_qemu_script : bool = conf["ctf"].get("use-custom-qemu-script", False)
        if self.use_custom_qemu_script:
            printer.note("use custom qemu script")

    
class Config:
    '''
    parse user/sys config file (current use .json).
    '''
    SYS_CONF  = Path.cwd() / "config" / "sys.json"
    USER_CONF = Path.cwd() / "config" / "user.json"

    def __init__(self) -> None:

        # sanity and simple check for cwd
        cwd = Path.cwd()
        ck = cwd / "autokd"
        if not ck.is_dir():
            printer.fatal(f"{ck.name} not found, maybe in incorrect directory")


        # url path
        self.docker_url              : str  = None
        self.linux_url               : str  = None
        self.kernel_version          : str  = None
        self.linux_target_name       : str  = None # merely name
        self.linux_target_path       : Path = None # full path
        self.download_url            : str  = None
        self.unpacked_dir_name       : str  = None # e.g. linux-2.6.0
        self.kernel_root_dir         : Path = None #
        self.__bziamge_path          : Path = None
        self.initrd_path             : Path = None
        self.modified_initrd_path    : Path = None
        self.initrd_is_root_used     : bool = False

        # dir path TODO: reconstruct here
        def create_if_not_exist(p : Path) -> None:
            if not p.exists():
                p.mkdir()
            
        self.resource_dir_path       : Path = cwd / "resource"
        self.scripts_dir_path        : Path = cwd / "scripts"
        self.unpacked_fs_dir_path    : Path = cwd / "fs-root"
        self.kernel_preroot_dir_path : Path = cwd / "kernel-root" # not real root
        self.download_dir_path       : Path = cwd / "download"

        create_if_not_exist(self.resource_dir_path)
        create_if_not_exist(self.scripts_dir_path)
        create_if_not_exist(self.unpacked_fs_dir_path)
        create_if_not_exist(self.kernel_preroot_dir_path)
        create_if_not_exist(self.download_dir_path) 

        # qemu
        self.__qemu_script_path      : Path = self.scripts_dir_path / "qemu-run.sh"
        
        # exp
        self.exp_src_path            : Path = cwd /  "./exp.c"

        # qemu options
        self.qemuopts                : QemuConfig = None

        # msic 
        self.msicopts                : MsicConfig = None

        # ctf
        self.ctfopts                 : CtfConfig = None 

    def parse(self) -> None:
        try:
            with open(self.SYS_CONF) as sysf:
                conf = json.load(sysf)
                self.docker_url      : str = conf["docker-url"]  # e.g : squirre17/dirtypipe:1.0 TODO: remove it 
                self.linux_url       : str = conf["linux-url"]    
                self.image_name      : str = self.docker_url.split("/")[1] # e.g. squirre17/dirtypipe:1.0 => dirtypipe:1.0 
                self.kernel_src_path : str = Path.cwd() / "kernel-src"

        except FileNotFoundError:
            printer.fatal("{} not found".format(os.path.abspath(self.SYS_CONF)))
        
        try:# TODO:
            with open(self.USER_CONF) as userf:
                conf = json.load(userf)
                self.nproc               : int  = conf["nproc"]
                self.kernel_version      : str  = conf["kernel-version"] # e.g. v5.10-rc1                
                self.initrd_is_root_used : bool = conf["initrd-is-root-used"] # TODO optimize here for empty key judge
                self.qemuopts                   = QemuConfig(conf)
                self.msicopts                   = MsicConfig(conf)
                self.ctfopts                    = CtfConfig(conf)
        except Exception:
            raise Exception

    @property
    def bziamge_path(self) -> Path:
        if self.ctfopts.enabled:
            return self.ctfopts.bzimage_path
        else:
            return self.__bziamge_path

    @bziamge_path.setter
    def bziamge_path(self, path : Path) -> None:
        self.__bziamge_path = path

    @property
    def qemu_script_path(self) -> Path:
        if self.ctfopts.use_custom_qemu_script:
            return Path.cwd() / "qemu-custom.sh"
        else:
            return self.__qemu_script_path
    
    @qemu_script_path.setter
    def qemu_script_path(self, path : Path) -> None:
        self.__qemu_script_path = path
        
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

    



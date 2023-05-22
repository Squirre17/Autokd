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

class Kbuilder:
    '''
    kernel builder : be responsible for kernel donwload, unpack, cmopile and clean so on
    '''

    DOWNLOAD_PATH : Path = Path.absolute(Path.cwd() / "download")
    
    def __init__(self) -> None:
        # self.kernel_src_path : Path = config.kernel_src_path # full path
        config.target_name        : str  = "linux-" + config.kernel_version + ".tar.gz"                      # full path
        config.target_path        : Path = self.DOWNLOAD_PATH / config.target_name
        config.download_url       : str  = "{url}/{target}".format(
            url = config.linux_url,
            target = config.target_name
        )
        config.kernel_preroot_dir : Path = Path.cwd() / "kernel-root" # not real root
        config.unpacked_dir_name  : str  = config.target_name.replace(".tar.gz", "") # convert linux-2.6.0.tar.gz => linux-2.6.0
        config.kernel_root_dir    : Path = config.kernel_preroot_dir / config.unpacked_dir_name
        config.resource_dir_path       : Path = Path.cwd() / "resource"
        config.initrd_path        : Path = config.resource_dir_path / "initrd.cpio"

        # temp
        self.nproc = 2

    def download(self) -> Type['Kbuilder']:
        '''
        e.g. : wget https://mirrors.edge.kernel.org/pub/linux/kernel/v2.6/linux-2.6.0.tar.gz
                url is https://mirrors.edge.kernel.org/pub/linux/kernel/v2.6 TODO:
        '''
        if not self.DOWNLOAD_PATH.exists():
            printer.note(f"make dir on {self.DOWNLOAD_PATH}")
            self.DOWNLOAD_PATH.mkdir()
        
        if config.target_path.exists():
            printer.note(f"{config.target_path} exists, skip download...")
            return self
        
        printer.info(f"Downloading {config.download_url} ... This may take a while!")
        # TODO:
        # with Dynbar(unit = "B", unit_scale = True, miniters = 1, desc = self.target_file.name) as t:
        #     try:
        #         urllib.request.urlretrieve(
        #             self.download_url, filename=self.target_file, reporthook = t.update_to
        #         )
        #         t.total = t.n
        #     except urllib.error.HTTPError:
        #         printer.fatal(f"{target_file} didn't exist")
        def redownload(url, filename):
            try:
                urllib.request.urlretrieve(config.download_url, filename=config.target_path.absolute())
            except urllib.error.ContentTooShortError:
                redownload(url, filename)

        try:
            redownload(config.download_url, filename=config.target_path.absolute())
        except urllib.error.HTTPError:
            printer.fatal(f"{config.download_url} didn't exist")
        return self
    
    def unpack(self) -> Type['Kbuilder']:
        '''
        unpack a tgz
        '''

        # sanity check for skip unpack
        if config.kernel_preroot_dir.exists() and len([_ for _ in config.kernel_preroot_dir.iterdir()]) != 0:
            printer.note("root dir exist, do not unpack again")
            return self
        else:
            try:
                config.kernel_preroot_dir.mkdir()
            except FileExistsError:
                pass

        printer.info("Unpacking kernel src tgz...")
        try:
            # add a check for download integrity
            try:
                with tarfile.open(config.target_path, mode="r") as t:
                    members = t.getmembers()
                    for member in tqdm(iterable=members, total=len(members)):
                        t.extract(member, config.kernel_preroot_dir)
            except EOFError:
                printer.fatal(f"{config.target_name} incomplete, abort (remove it and try again)")

            return self
        except tarfile.TarError:
            printer.fatal("Failed to extract tar kernel archive!")

        printer.dbg("todo unpack")
        return self

    def compile(self) -> Type['Kbuilder']:

        kconf = config.kernel_root_dir / ".config"
        config.bzimage_path = config.kernel_root_dir / "arch/x86_64/boot/bzImage"
        assert config.bzimage_path.exists()
        
        for iter in config.kernel_root_dir.iterdir():
            if iter.name == "vmlinux":
                printer.note("vmlinux detected, use the old")
                return self

        cur_dir = Path.cwd()

        if kconf.exists():
            printer.note("kernel .config file found, skip config generate stage")
        else:
            os.chdir(config.kernel_root_dir)
            sp.run("make x86_64_defconfig", shell=True)
            sp.run("make menuconfig", shell=True)
            os.chdir(cur_dir)

        self.check_debug_config()# TODO: ugly now

        cmd = f"make bzImage -j{self.nproc}"
        printer.note(f"start to compile kernel with nproc({self.nproc})")
        os.chdir(config.kernel_root_dir)
        logger.debug(config.kernel_root_dir)
        sp.run(cmd, shell=True)
        os.chdir(cur_dir)

        printer.info("kernel build success!")
        return self
    
    def make_mrproper(self) -> Type['Kbuilder']:
        raise NotImplementedError
        return self
    
    def check_debug_config(self) -> Type['Kbuilder']:
        '''
        make sure some debug config is 'y' in `.config`
        '''

        DEBUG_OPTIONS : List[str] = [
            # 设置调试符号
            "CONFIG_DEBUG_INFO",
            # fuse 开启，一些漏洞利用会用到
            "CONFIG_FUSE_FS", 
            # VIPC 开启，可以使用msg系列
            "CONFIG_SYSVIPC",
            "CONFIG_SYSVIPC_SYSCTL",
            "CONFIG_SYSVIPC_COMPAT",
            # 设置这个才能正确调用msg 里的copy 系列函数
            "CONFIG_CHECKPOINT_RESTORE", 
            # gdb 源码级别调试
            "CONFIG_DEBUG_INFO_DWARF4",
        ]

        dot_config : Path = config.kernel_root_dir / ".config" 
        if not dot_config.exists() or not dot_config.is_file():
            printer.fatal(f"{dot_config} can't found")
        
        '''
        e.g.

        # Linux/x86 5.10.0-rc1 Kernel Configuration
        #
        CONFIG_CC_VERSION_TEXT="gcc (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0"
        CONFIG_CC_IS_GCC=y
        CONFIG_GCC_VERSION=90400
        CONFIG_LD_VERSION=234000000
        CONFIG_CLANG_VERSION=0
        '''
        with open(dot_config) as f: # DELAY_TODO: can optimize here

            lines = f.readlines()
            for line in lines:
                
                if line.startswith("#"):
                    continue
                
                for option in DEBUG_OPTIONS:
                    if line.startswith(option):
                        key, val = line.strip().split("=", 1)
                        assert key == option, f"{key} != {option}"
                        printer.err(f"option `{val}` set to `{key}`") if val != 'y' else ...

        printer.info("all .config options sanity check pass")

kbuilder = Kbuilder()




class Kunpacker:
    def __init__(self) -> None:
        pass




# class Kdownloader: # not need?
#     '''
#     TODO:
#     '''

#     def __init__(self) -> None:
#         raise NotImplementedError
    
#     def resources(self) -> Type["Kdownloader"]:
#         '''
#         download resources
#         '''
#         cmd = "git https://github.com/Squirre17/autokd-resources.git resource"

#         config.resouce_path = Path.cwd() / "resource"
#         if config.resouce_path.exists() and len([_ for _ in config.resouce_path.iterdir()]) != 0:
#             printer.note("resource dir exist, do not download again")
#             return self

#         printer.note("download resource, this will take a while")
#         sp.run(cmd, shell=True)




import akd.utils.printer as printer

from pathlib    import (Path)
from typing     import (List)
from akd.config import (config)

class Kbuilder:
    '''
    kernel builder : be responsible for kernel donwload, unpack, cmopile and clean so on
    '''
    
    def __init__(self) -> None:
        self.kernel_src_path : Path = config.kernel_src_path
        ...
    
    def download(self) -> None:
        raise NotImplementedError
    
    def unpack(self) -> None:
        raise NotImplementedError

    def compile(self) -> None:
        raise NotImplementedError
    
    def make_mrproper(self) -> None:
        raise NotImplementedError
    
    def check_debug_config(self) -> None:
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

        dot_config : Path = self.kernel_src_path / ".config" 
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









class Kdownloader:
    '''
    TODO:
    '''

    def __init__(self) -> None:
        raise NotImplementedError
import os
import json
import akd.utils.printer as printer

class Config:
    '''
    parse user/sys config file (current use .json).
    '''
    SYS_CONF  = "./config/sys.json"
    USER_CONF = "./config/user.json"

    def __init__(self) -> None:

        self.__docker_url : str = ""
        self.__linux_url  : str = ""
        pass

    def parse(self) -> None:
        try:
            with open(self.SYS_CONF) as sysf:
                conf = json.load(sysf);
                self.__docker_url : str = conf["docker-url"]
                self.__linux_url  : str = conf["liunx-url"]    
        except FileNotFoundError:
            printer.fatal("{} not found".format(os.path.abspath(self.SYS_CONF)))
        
        try:# TODO:
            with open(self.USER_CONF) as userf:

                pass
        except Exception:
            raise Exception
    
    @property
    def docker_url(self) -> str:
        return self.__docker_url
    

config = Config()
config.parse()


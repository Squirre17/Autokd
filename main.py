import sys

from autokd.initrd   import initrd
from autokd.kdocker  import kdocker 
from autokd.checker  import checker
from autokd.kbuilder import kbuilder
from autokd.krunner  import krunner
from autokd.config   import config
import autokd.utils.printer as printer

def run():
    checker.proxy()
    kbuilder.download().unpack().compile()
    initrd.unpack().pack()
    krunner.make_run_script().compile_exp().run()
    # kbuilder.unpack()
    # kbuilder.()

def ctf():
    if not config.ctfopts.enabled:
        printer.fatal("only enable ctf option in user.json can use ctf mode")
        
    initrd.unpack().pack()
    krunner.make_run_script().compile_exp().run()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        printer.fatal("Usage : python3 main.py <option>")
    
    opt = sys.argv[1]
    if opt == "run":
        run()
    elif opt == "ctf":
        ctf()
    else:
        raise RuntimeError

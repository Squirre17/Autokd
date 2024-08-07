import sys

from autokd.extractor import extractor
from autokd.kbuilder  import kbuilder
# from autokd.kdocker   import kdocker 
from autokd.checker   import checker
from autokd.krunner   import krunner
from autokd.initrd    import initrd
from autokd.config    import config
import autokd.utils.printer as printer

def run():
    if config.ctfopts.enabled:
        printer.fatal("ctf option is conflict with `./akd run`")
        
    checker.proxy()
    kbuilder.download().unpack().compile()
    initrd.unpack().compile_exp().pack()
    krunner.make_run_script().run()
    # kbuilder.unpack()
    # kbuilder.()

def ctf():
    if not config.ctfopts.enabled:
        printer.fatal("only enable ctf option in user.json can use ctf mode")
    extractor.extract_vmlinux()
    initrd.unpack().compile_exp().pack()
    krunner.make_run_script().run()

if __name__ == "__main__":
    
    if len(sys.argv) > 3 or len(sys.argv) < 2:
        printer.fatal("Usage : python3 main.py <option>")
    
    opt = sys.argv[1]
    if len(sys.argv) == 3:
        if sys.argv[2] == "skip":
            config.msicopts.need_confirm = False

    if opt == "run":
        run()
    elif opt == "ctf":
        ctf()
    else:
        raise RuntimeError

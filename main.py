from autokd.initrd   import initrd
from autokd.kdocker  import kdocker 
from autokd.checker  import checker
from autokd.kbuilder import kbuilder
from autokd.krunner  import krunner
import autokd.utils.printer as printer

def main():
    checker.proxy()
    kbuilder.download().unpack().compile()
    initrd.unpack().pack()
    krunner.make_run_script().compile_exp().run()
    # kbuilder.unpack()
    # kbuilder.()


main()
from akd.initrd   import initrd
from akd.kdocker  import kdocker 
from akd.checker  import checker
from akd.kbuilder import kbuilder
from akd.krunner  import krunner
import akd.utils.printer as printer

def main():
    checker.proxy()
    kbuilder.download().unpack().compile()
    initrd.unpack().pack()
    krunner.make_run_script().run()
    # kbuilder.unpack()
    # kbuilder.()


main()
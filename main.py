from akd.initrd   import initrd
from akd.kdocker  import kdocker 
from akd.checker  import checker
from akd.kbuilder import kbuilder
import akd.utils.printer as printer

def main():
    checker.proxy()
    kbuilder.download().unpack().compile()
    initrd.unpack().pack()

    # kbuilder.unpack()
    # kbuilder.()


main()
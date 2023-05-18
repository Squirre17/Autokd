from akd.kdocker  import kdocker 
from akd.checker  import checker
from akd.kbuilder import kbuilder
import akd.utils.printer as printer

def main():
    checker.proxy()
    kbuilder.download().unpack().compile()
    # kbuilder.unpack()
    # kbuilder.()


main()
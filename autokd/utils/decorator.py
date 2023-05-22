'''
all decorators
'''
import time
import functools
import autokd.utils.printer as printer

from typing          import (Callable, Any)
from autokd.utils.color import (Color)


def deprecated(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(Color.redify(f"WARNING : this function `{func}` have been deprecated"))
        return func(*args, **kwargs)
    return wrapper

def timer(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args , **kwargs) -> Any:
        start = time.time()
        ret = func(*args, **kwargs)
        end   = time.time()
        printer.note("function {} spend {:0.8f} ms".format(func.__name__, (end - start) * 1000))
        return ret
    return wrapper

def debug_wrapper(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args , **kwargs) -> Any:
        printer.dbg(f"function -> {func.__name__} : START")
        ret = func(*args, **kwargs)
        printer.dbg(f"function -> {func.__name__} : END")
        return ret
    return wrapper

import traceback
def handle_exception(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args , **kwargs) -> Any:
        try :
            return func(*args, **kwargs)
        except Exception as e :
            printer.err("Exception occur!")
            print(traceback.format_exc())
    return wrapper
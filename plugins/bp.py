'''
for facilitate gdb breakpoint
'''
import gdb
import functools
import autokd.utils.printer as printer
from typing import Callable, Any

ulp = gdb.lookup_type('unsigned long').pointer()

def only_when_running(func):

    @functools.wraps(func)
    def wrapper(*args):
        if gdb.selected_inferior() is None:
            print("[-] Process is not running, cannot use this cmd")
            return
        return func(*args)
    return wrapper

import traceback
def handle_exception(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args , **kwargs) -> Any:
        try :
            return func(*args, **kwargs)
        except:
            print("[-] Exception occur!")
            print(traceback.format_exc())
    return wrapper

class BreakpointAtDriverAddr(gdb.Command):
    def __init__(self):
        super().__init__("bda", gdb.COMMAND_USER)

    driver_base_addr : int = None

    @only_when_running
    @handle_exception
    def invoke(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        if len(args) != 2:
            printer.err("Usage: bda set <driver base addr> / bda <op> <offset>")
            print(args)
            return
        
        if args[0] != "set" and self.driver_base_addr is None:
            printer.err("driver_base_addr not set, do `bda set <driver base addr>` in advance")
            return
        
        if args[0] == "set":
            self.driver_base_addr = int(args[1], 16) # ValueError
            printer.info("driver_base_addr be set to 0x{:x}".format(self.driver_base_addr))
            return
        elif args[0].startswith("b"): # assume a breakpoint cmd
            cmd = "{} *(0x{:x} + {})".format(args[0], self.driver_base_addr, args[1])
            printer.info(cmd)
            gdb.execute(cmd)
            return
        elif args[0].startswith("x"): # assume a x/4gx basea + offset
            cmd = "{} 0x{:x} + {}".format(args[0], self.driver_base_addr, args[1])
            printer.info(cmd)
            try:
                gdb.execute(cmd)
            except gdb.MemoryError:
                print("")
                printer.err("Cannot access memory at address 0x{:x}".format(self.driver_base_addr + int(args[1], 16)))
            return
        else:
            printer.err("not support yet")
            return


BreakpointAtDriverAddr()

class BreakpointAtKernelAddr(gdb.Command):
    def __init__(self):
        super().__init__("bka", gdb.COMMAND_USER)

    kernel_base_addr : int = None

    @only_when_running
    @handle_exception
    def invoke(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        if len(args) != 2:
            printer.err("Usage: bka set <kernel base addr> / bka <op> <offset>")
            print(args)
            return
        
        if args[0] != "set" and self.kernel_base_addr is None:
            printer.err("kernel_base_addr not set, do `bka set <kernel base addr>` in advance")
            return
        
        if args[0] == "set":
            self.kernel_base_addr = int(args[1], 16) # ValueError
            printer.info("kernel_base_addr be set to 0x{:x}".format(self.kernel_base_addr))
            return
        elif args[0].startswith("b"): # assume a breakpoint cmd
            cmd = "{} *(0x{:x} + {})".format(args[0], self.kernel_base_addr, args[1])
            printer.info(cmd)
            gdb.execute(cmd)
            return
        elif args[0].startswith("x"): # assume a x/4gx basea + offset
            cmd = "{} 0x{:x} + {}".format(args[0], self.kernel_base_addr, args[1])
            printer.info(cmd)
            try:
                gdb.execute(cmd)
            except gdb.MemoryError:
                print("")
                printer.err("Cannot access memory at address 0x{:x}".format(self.kernel_base_addr + int(args[1], 16)))
            return
        else:
            printer.err("not support yet")
            return

BreakpointAtKernelAddr()
import sys
import traceback

from akd.utils.color import Color

def info(msg):
    prompt = Color.colorify("[+]" ,"green")
    body   = " INFO  : "
    print(prompt + body, end = "")
    print(msg)

in_debug = True

def dbg(msg):
    if in_debug:
        prompt = Color.colorify("[#]" ,"purple")
        body   = " DBG   : "
        print(prompt + body, end = "")
        print(msg)
    else : pass

def err(msg):
    prompt = Color.colorify("[!]" ,"red")
    body   = " ERR   : "
    print(prompt + body, end = "")
    print(msg)

def fatal(msg):
    '''
    fatal err by program
    '''
    prompt = Color.boldify(Color.colorify("[!]" ,"red"))
    body   = " FATAL : "
    print(prompt + body, end = "")
    print(msg)
    sys.exit(1)


def warn(msg):
    prompt = Color.colorify("[-]" ,"yellow")
    body   = " WARN  : "
    print(prompt + body, end = "")
    print(msg)

def note(msg):
    prompt = Color.colorify("[*]" ,"blue")
    body   = " NOTE  : "
    print(prompt + body, end = "")
    print(msg)


def err_print_exc(msg):
    err(msg)
    traceback.print_exc()

if __name__ == "__main__":
    s = "123"
    info(s)
    dbg(s)
    err(s)
    note(s)
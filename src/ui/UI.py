import curses
import threading
import os

## https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124
YELLOW = "\x1b[0;33m"
WHITE = "\x1b[0;37m"
RED = "\x1b[0;31m"
BLUE = "\x1b[0;34m"
CYAN = "\x1b[0;36m"

BOLD_RED = "\x1b[1;31m"

## https://stackoverflow.com/questions/12492810/python-how-can-i-make-the-ansi-escape-codes-to-work-also-in-windows
def init():
    os.system("")
    


def print_colour(text,colour):
    print("{}{}{}".format(colour,text,WHITE),end="")



def diagnostic(name,value,suffix=""):
    print_colour("{}: {} {}\n".format(name,str(value),suffix),YELLOW)


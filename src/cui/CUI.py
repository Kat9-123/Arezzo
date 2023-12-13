"""Module that handles the Console User Interface"""


import cui.Progress as Progress
from core.Constants import *
from core.Configurator import CONFIG

import os




## https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124
YELLOW = "\x1b[0;33m"
WHITE = "\x1b[0;37m"
RED = "\x1b[0;31m"
BLUE = "\x1b[0;34m"
PURPLE = "\x1b[0;35m"
CYAN = "\x1b[0;36m"
GREEN = "\x1b[0;32m"

BOLD_RED = "\x1b[1;31m"



HIDE_CONSOLE_CURSOR = "\033[?25l"


spinner = None


def setY(y):
    print("\033[{};{}H".format(y,1))


def yesno() -> bool:
    answer = input(">")
    answer = answer.lower()

    if answer == "y" or answer == "yes":
        return True
    
    return False

def init():
    ## https://stackoverflow.com/questions/12492810/python-how-can-i-make-the-ansi-escape-codes-to-work-also-in-windows
    ## Required for colours
    os.system("")



    # Hide console cursor
    print(HIDE_CONSOLE_CURSOR, end="")







def set_colour(colour):
    print(colour,end="")




def warning(value):
    print_colour(f"{str(value)}\n",RED)



def debug(value,*,end="\n",debugControl=True):
    if debugControl and not CONFIG["DEBUG"]["blanket_disable_debug_print"]:
        print_colour(value,colour=WHITE,end=end)

def print_colour(text,colour,*,end="",debugControl=True):
    if debugControl:
        print(f"{colour}{text}{WHITE}",end=end)



def diagnostic(name,value,suffix="",*,end="\n"):
    print_colour(f"{name}: {value} {suffix}",WHITE,end=end)



def newline(*,debugControl=True):
    if debugControl:
        print()

def important(text,*,end="\n"):
    print_colour(text,CYAN,end=end)


def progress(value,*,spin=False,finishedText=""):
    """Create a spinner"""
    if finishedText == "":
        finishedText = value
    Progress.progress(value,spin,finishedText)


def force_stop_progress(succesful=True):
    Progress.force_finish(succesful)



def notify():
    print("\a")
import cui.CUI as CUI
import threading
import time
from core.Configurator import CONFIG


FRAMES = [
    # "     ",
    ".    ",
    "..   ",
    "...  ",
    " ... ",
    "  ...",
    "   ..",
    "    .",
    #"     ",
    "    .",
    "   ..",
    "  ...",
    " ... ",
    "...  ",
    "..   ",
    ".    ",

]

currentText = ""

def progress(text,spin=False) -> None:
    global currentText


    __finish(currentText)
    currentText = text

    if spin and CONFIG["DEBUG"]["spin"]:
        __start_spinning(currentText)
        return

    CUI.print_colour(f"[.....] {currentText}",CUI.GREEN,end="\n")


def force_finish() -> None:
    __finish(currentText)

def __finish(text) -> None:
    if text == "":
        return

    if __stop_spinner():
        return

    CUI.print_colour(f"[  √  ] {text}",CUI.GREEN,end="\n\n")




spinnerThread = None
spinnerStopEvent = None
spinnerText = ""
def __start_spinning(text):
    global spinnerThread,spinnerStopEvent,spinnerText

    spinnerThread = threading.Thread(target=__spin)
    spinnerStopEvent = threading.Event()
    spinnerText = text
    spinnerThread.start()


def __spin():
    i = 0
    while True:
        time.sleep(0.06)

        CUI.print_colour(f"[{FRAMES[i]}] {spinnerText}", CUI.GREEN, end="\r")


        i += 1
        i %= len(FRAMES)

        if spinnerStopEvent.is_set():
            return

def __stop_spinner() -> bool:
    global spinnerThread, spinnerStopEvent,spinnerText,currentText
    if spinnerThread == None:
        return False

    currentText = ""
    spinnerStopEvent.set()
    spinnerThread.join()

    spinnerThread = None


    CUI.print_colour(f"[  √  ] {currentText}\n",CUI.GREEN,end="\n")
    return True
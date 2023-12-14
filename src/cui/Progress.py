import cui.CUI as CUI
import threading
import time

SPIN_ENABLED = True


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

currentFinishedText = ""

def progress(text,spin=False,finishedText="") -> None:
    global currentFinishedText


    __finish(currentFinishedText)
    currentFinishedText = finishedText

    if spin and SPIN_ENABLED:
        __start_spinning(text)
        return

    CUI.print_colour(f"[.....] {text}",CUI.GREEN,end="\n")


def force_finish(succesful) -> None:
    __finish(currentFinishedText,succesful)

def __finish(text,succesful=True) -> None:
    if text == "":
        return

    if __stop_spinner(succesful):
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

def __stop_spinner(succesful=True) -> bool:
    global spinnerThread, spinnerStopEvent,spinnerText,currentFinishedText
    if spinnerThread == None:
        return False

    
    spinnerStopEvent.set()
    spinnerThread.join()

    spinnerThread = None

    if succesful:
        CUI.print_colour(f"[  √  ] {currentFinishedText}\n",CUI.GREEN,end="\n")
    else:
        CUI.print_colour(f"[  x  ] {currentFinishedText}\n",CUI.RED,end="\n")
    currentFinishedText = ""
    return True
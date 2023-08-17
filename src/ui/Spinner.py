import time
import threading
import ui.UI as UI


class Spinner:


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

    thread: any
    stopEvent: any

    text: str

    def __init__(self,_text) -> None:
        self.thread = threading.Thread(target=self.__run)
        self.stopEvent = threading.Event()
        self.text = _text

        return
        self.thread.start()
    
    def __run(self):
        i = 0
        while True:
            time.sleep(0.06)

            UI.print_colour(f"[{self.FRAMES[i]}] {self.text}", UI.GREEN, end="\r")

            i += 1
            if i >= len(self.FRAMES):
                i = 0

            if self.stopEvent.is_set():
                return
    
    def stop(self):
        return
        self.stopEvent.set()
        self.thread.join()

        UI.set_colour(UI.GREEN)
        print(f"[  √  ] {self.text}\n")
        UI.set_colour(UI.WHITE)
        


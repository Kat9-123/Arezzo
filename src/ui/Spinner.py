import time
import threading



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

        
        self.thread.start()
    
    def __run(self):
        i = 0
        while True:
            time.sleep(0.06)

            print("[{}] {}".format(self.FRAMES[i],self.text),end="\r")

            i += 1
            if i >= len(self.FRAMES):
                i = 0
            if self.stopEvent.is_set():
                return
    
    def stop(self):
        self.stopEvent.set()
        self.thread.join()
        print("[  V  ] {}".format(self.text))
        


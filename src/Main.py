# MY_CONSTANT
# my_function
# myValue
# MyClass

# __privateFunction
# _overridableFunction
import Utils
import Graphing
import AudioProcessor
import NoteGenerator
import ui.UI as UI
import SheetMusicGenerator


import time





voiceCount = 1

AUDIO_TO_ANALYSE = r"PWS_TEST_5.wav"





outputName = "{}_{}".format(str(int(time.time())),AUDIO_TO_ANALYSE)

AUDIO_BASE_PATH = "audio"





def start():

    
    #curses.wrapper(test)
    UI.init()



    Graphing.create_plot(rows=4)


    spectrum,chroma,onset,rawTempo = AudioProcessor.process_audio("{}/{}".format(AUDIO_BASE_PATH,AUDIO_TO_ANALYSE))

    voices, correctedTempo = NoteGenerator.get_notes_voices(spectrum,chroma,onset,rawTempo)

    SheetMusicGenerator.midi(voices,correctedTempo)


    Graphing.save_plot()
    Graphing.show_plot()


if __name__ == "__main__":
    start()


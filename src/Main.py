# MY_CONSTANT
# my_function
# myValue
# MyClass

# __privateFunction
# _overridableFunction




import Graphing
import AudioProcessor
import NoteGenerator
import ui.UI as UI
import SheetMusicGenerator


import time




#"C:\Program Files\MuseScore 4\bin\MuseScore4.exe" -o "Test.pdf" C:\Users\trist\Documents\transcription\output\1690117354_PWS_TEST_7.wav.mid

MUSECORE4_PATH = "C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe"

EXPORT_TYPE = "pdf" # PNG or PDF


AUDIO_TO_ANALYSE = r"PWS_TEST_4.wav"





outputName = "{}_{}".format(str(int(time.time())),AUDIO_TO_ANALYSE)

AUDIO_BASE_PATH = "audio"





def start():

    
    
    UI.init()

   

    Graphing.create_plot(rows=3)


    spectrum,chroma,onset,rawTempo = AudioProcessor.process_audio("{}/{}".format(AUDIO_BASE_PATH,AUDIO_TO_ANALYSE)) 

    voices, correctedTempo = NoteGenerator.get_notes_voices(spectrum,chroma,onset,rawTempo)

    SheetMusicGenerator.midi(voices,correctedTempo)


    Graphing.save_plot()

    UI.print_colour("\nDone, showing plots.\n",UI.GREEN)

    Graphing.show_plot()


if __name__ == "__main__":
    start()


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
import Utils
import Scoring

import time




MUSECORE4_PATH = "C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe"

EXPORT_TYPE = "pdf" # PNG or PDF


AUDIO_TO_ANALYSE = r"PWS_TEST_2.wav"


COMPARE_FILE = r"PWS_TEST_4.mid"





outputName = f"{str(int(time.time()))}_{AUDIO_TO_ANALYSE}"

AUDIO_BASE_PATH = "audio"





def start():

    startTime = time.perf_counter() 
    
    UI.init()




    Graphing.create_plot(rows=3)


    processedAudioData = AudioProcessor.process_audio(f"{AUDIO_BASE_PATH}\\{AUDIO_TO_ANALYSE}") 

    notes = NoteGenerator.get_notes(processedAudioData)
    
    SheetMusicGenerator.midi(notes,processedAudioData.tempo)


    Graphing.save_plot()


    duration = time.perf_counter() - startTime
    perSecondOfAudioDuration = duration/processedAudioData.duration

   
   # Scoring.score(notes,COMPARE_FILE,processedAudioData.tempo)
    UI.newline()
   
    UI.diagnostic("Processing time per second of audio",round(perSecondOfAudioDuration,3), "seconds")
    UI.print_colour(f"\nDone. Processing {round(processedAudioData.duration,3)} seconds of audio took {round(duration, 3)} seconds. Showing plots.\n",UI.GREEN)

    
    Graphing.show_plot()


if __name__ == "__main__":
    start()


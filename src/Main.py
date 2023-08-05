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





outputName = f"{str(int(time.time()))}_{AUDIO_TO_ANALYSE}"

AUDIO_BASE_PATH = "audio"





def start():

    startTime = time.perf_counter()
    
    UI.init()

   

    Graphing.create_plot(rows=3)


    processedAudioData = AudioProcessor.process_audio(f"{AUDIO_BASE_PATH}\\{AUDIO_TO_ANALYSE}") 

    voices, correctedTempo = NoteGenerator.get_notes_voices(processedAudioData)

    SheetMusicGenerator.midi(voices,correctedTempo)


    Graphing.save_plot()


    duration = time.perf_counter() - startTime
    perSecondOfAudioDuration = duration/processedAudioData.duration


    UI.diagnostic("Processing time per second of audio",round(perSecondOfAudioDuration,3), "seconds")
    UI.print_colour(f"\nDone. Processing {round(processedAudioData.duration,3)} seconds of audio took {round(duration, 3)} seconds. Showing plots.\n",UI.GREEN)

    
    Graphing.show_plot()


if __name__ == "__main__":
    start()


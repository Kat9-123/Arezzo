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
import testing.Tester as Tester
import SheetMusicGenerator
import Utils
import Scoring

import Config as cfg

import time















def main():
    cfg.get_configuration()

    UI.init()
    run(cfg.CONFIG["path"])
    #Tester.test()
    #score = run(f"{AUDIO_BASE_PATH}\\{AUDIO_TO_ANALYSE}",testMode=True)
    






def run(path,*,testMode=False,tempoOverride=-1):
    startTime = time.perf_counter() 

    UI.print_colour(f"Processing {path}",UI.GREEN,end="\n\n")
    

    if not testMode:
        Graphing.create_plot(rows=3)


    processedAudioData = AudioProcessor.process_audio(path,tempoOverride) 


    notes = NoteGenerator.get_notes(processedAudioData)
    
    if not testMode:
        SheetMusicGenerator.generate_midi_file(notes,processedAudioData.tempo)

    if not testMode:
        Graphing.save_plot()


    duration = time.perf_counter() - startTime
    perSecondOfAudioDuration = duration/processedAudioData.duration

   
    
    UI.newline()
   
    UI.diagnostic("Processing time per second of audio",round(perSecondOfAudioDuration,3), "seconds")
    UI.print_colour(f"\nDone. Processing {round(processedAudioData.duration,3)} seconds of audio took {round(duration, 3)} seconds. Showing plots.\n",UI.GREEN)


    if not testMode:
        Graphing.show_plot()
    return (notes,processedAudioData.tempo)


    

if __name__ == "__main__":
    main()


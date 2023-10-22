# MY_CONSTANT
# my_function
# myValue
# MyClass

# __privateFunction
# _overridableFunction

# The first thing we do is load the config. Because we do this
# before initialising anything else, the global var CONFIG can
# just be imported directly by other scripts
import Configurator as cfg
cfg.get_configuration()


import time
import os


from Configurator import CONFIG, Modes, mode
import Graphing
import AudioProcessor
import NoteGenerator
import cui.CUI as CUI
import testing.Tester as Tester
import SheetMusicGenerator
import network.Manager as Manager

import network.Trainer as NetTrainer
import network.TrainingDataProcessor as TrainingDataProcessor
import KeyFinder, TimeSigFinder

#import network.training.RandomMIDIGenerator as RAND











def main() -> None:

    
    CUI.init()

    if mode == Modes.PROCESS_TRAINING_DATA:
        print("Processing training data...")
        TrainingDataProcessor.process_training_data()
        return

    elif mode == Modes.TRAIN:
        print("Training network...")
        NetTrainer.train()
        return

    elif mode == Modes.TEST_MULTIPLE:
        print("Testing...")
        Tester.test()
        return

    elif mode == Modes.TEST_SINGLE:
        raise Exception("Single test mode hasnt been implemented yet!")

    # Standard mode.
    run(CONFIG["ARGS"]["audio"])





def run(path,*,testMode=False,tempoOverride=-1) -> (list,float):
    print("Generating sheet music...")
    startTime = time.perf_counter()
    Manager.setup_trained_model()
    outputName = f"{str(int(time.time()))}_{os.path.basename(path)}"

    CUI.print_colour(f"Processing {path}",CUI.GREEN,end="\n\n")
    

    if not testMode:
        Graphing.create_plot(rows=3)


    processedAudioData = AudioProcessor.process_audio(path,tempoOverride) 


    notes = NoteGenerator.get_notes(processedAudioData)
    
    if not testMode:
        SheetMusicGenerator.generate_midi_file(notes,processedAudioData.tempo,outputName)

    if not testMode:
        Graphing.save_plot(outputName)

    KeyFinder.guess_key(notes)
    TimeSigFinder.guess_time_signature(notes)


    duration = time.perf_counter() - startTime
    perSecondOfAudioDuration = duration/processedAudioData.duration

   
    
    CUI.newline()
   
    CUI.diagnostic("Processing time per second of audio",round(perSecondOfAudioDuration,3), "seconds")
    CUI.print_colour(f"\nDone. Processing {round(processedAudioData.duration,3)} seconds of audio took {round(duration, 3)} seconds. Showing plots.\n",CUI.GREEN)


    if not testMode:
        Graphing.show_plot()
    return (notes,processedAudioData.tempo)


    

if __name__ == "__main__":
    main()


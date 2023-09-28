# MY_CONSTANT
# my_function
# myValue
# MyClass

# __privateFunction
# _overridableFunction




import Graphing
import AudioProcessor
import NoteGenerator
import cui.CUI as CUI
import testing.Tester as Tester
import SheetMusicGenerator
import network.Manager as Manager
import Utils
import Scoring
import network.Trainer as NetTrainer
import network.TrainingDataProcessor as TrainingDataProcessor

import Config as cfg

import time
import os
import pandas as pd


#import network.training.RandomMIDIGenerator as RAND











def main():

    cfg.get_configuration()
    CUI.init()



    if cfg.CONFIG["NETWORK"]["process_training_data"]:
        print("Processing training data...")
        TrainingDataProcessor.process_training_data()
        return

    if cfg.CONFIG["NETWORK"]["train_net"]:
        print("Training network...")
        NetTrainer.train()
        return

    if cfg.CONFIG["testing"]:
        print("Testing...")
        Tester.test()
        return


    Manager.setup_trained_model()

    print("Generating sheet music...")
    run(cfg.CONFIG["path"])
    ##    #score = run(f"{AUDIO_BASE_PATH}\\{AUDIO_TO_ANALYSE}",testMode=True)
    






def run(path,*,testMode=False,tempoOverride=-1):
    startTime = time.perf_counter()
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


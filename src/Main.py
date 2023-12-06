# MY_CONSTANT
# my_function
# myValue
# MyClass

# __privateFunction
# _overridableFunction
if __name__ == "__main__":
    print("Initialising...")



# The first thing we do is load the config. Because we do this
# before initialising anything else, the global var CONFIG can
# just be imported directly by other scripts
try:
    import core.Configurator as cfg
    cfg.get_configuration()


    import time
    import os


    from core.Configurator import CONFIG, Modes, mode
    import misc.Graphing as Graphing
    import core.AudioProcessor as AudioProcessor
    import transcription.NoteGenerator as NoteGenerator
    import cui.CUI as CUI
    import testing.Tester as Tester
    import transcription.SheetMusicGenerator as SheetMusicGenerator
    import network.Manager as Manager

    import network.Trainer as NetTrainer
    import network.TrainingDataProcessor as TrainingDataProcessor
    import transcription.KeyFinder as KeyFinder
    import transcription.TimeSigFinder as TimeSigFinder

    from transcription.ProcessedMusic import ProcessedMusic
except ModuleNotFoundError:
    from subprocess import Popen
    print("One or more module(s) were not found. Please see requirements.txt")
    print("or do you want to automatically install them? (yes/no)")
    x = input(">").lower()

    if x != 'y' and x != "yes":
        exit()
    print("Attempting to install dependencies...")
    Popen("pip install -r requirements.txt", shell=True).wait()
    exit()




def main() -> None:

    
    CUI.init()
    """
    test = Set.SpectrumDataset("learning\\spectra\\MAESTRO1.csd")

    print(len(test))
    print(test[0])

    with open("learning\\spectra\\MAESTRO1.csd", "rb") as f:
        header = f.read(8)
    
    headerArray = np.frombuffer(header,dtype=np.uint16)
    print(headerArray)

    _, _, sampleCount = compressor.__retrieve_header(headerArray)
    return
    """
    if mode == Modes.PROCESS_TRAINING_DATA:
        print("Processing training data...")
        TrainingDataProcessor.process_single()
        return
    
    elif mode == Modes.PROCESS_MULTIPLE_TRAINING_DATA:
        print("Processing multiple training data files...")
        TrainingDataProcessor.process_multiple()
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
        raise Exception("Single test mode hasn't been implemented yet!")

    # Standard mode.
    run(CONFIG["ARGS"]["audio"])





def run(path,*,testMode=False,tempoOverride=-1) -> (list,float):
    print("Generating sheet music...")
    startTime = time.perf_counter()

    

    Manager.setup_trained_model()
    outputName = f"{str(int(time.time()))}_{os.path.basename(path)}"

    CUI.print_colour(f"Processing {path}",CUI.GREEN,end="\n\n")
    

    if not testMode:
        Graphing.create_plot(rows=2)


    processedAudioData = AudioProcessor.process_audio(path,tempoOverride) 
    Graphing.show_plot()

    notes = NoteGenerator.get_notes(processedAudioData)

    key = KeyFinder.guess_key(notes)
    timeSig = TimeSigFinder.guess_time_signature(notes)

    processedMusic = ProcessedMusic(notes=notes,
                                    tempo=processedAudioData.tempo,
                                    key=key,
                                    timeSig=timeSig)

    if not testMode:
        SheetMusicGenerator.generate_midi_file(notes,processedAudioData.tempo,outputName)

    if not testMode:
        Graphing.save_plot(outputName)




    

    duration = time.perf_counter() - startTime
    perSecondOfAudioDuration = duration/processedAudioData.duration

   
    for file in os.listdir("temp\\"):
        os.remove(f"temp\\{file}")
    
    CUI.newline()
   
    CUI.diagnostic("Processing time per second of audio",round(perSecondOfAudioDuration,3), "seconds")
    CUI.print_colour(f"\nDone. Processing {round(processedAudioData.duration,3)} seconds of audio took {round(duration, 3)} seconds.\n",CUI.GREEN)


    if not testMode:
        Graphing.show_plot()
    return processedMusic


    



if __name__ == "__main__":
    main()


import time
import os


from core.Configurator import CONFIG
import misc.Graphing as Graphing
import core.AudioProcessor as AudioProcessor
import transcription.NoteGenerator as NoteGenerator
import cui.CUI as CUI

import transcription.SheetMusicGenerator as SheetMusicGenerator
import network.Manager as Manager


import transcription.KeyFinder as KeyFinder
import transcription.TimeSigFinder as TimeSigFinder

from transcription.ProcessedMusic import ProcessedMusic



def transcribe(path,*,testMode=False,tempoOverride=-1) -> (list,float):
    startTime = time.perf_counter()

    

    Manager.setup_trained_model()
    outputName = f"{str(int(time.time()))}_{os.path.basename(path)}"

   # CUI.print_colour(f"Processing {path}",CUI.GREEN,end="\n\n")
    

    if not testMode:
        Graphing.create_plot(rows=2)


    processedAudioData = AudioProcessor.process_audio(path,tempoOverride=tempoOverride)
    Graphing.show_plot()



    notes = NoteGenerator.get_notes(processedAudioData)

    key = KeyFinder.guess_key(notes)
    CUI.newline()
    timeSig = TimeSigFinder.guess_time_signature(notes)

    processedMusic = ProcessedMusic(notes=notes,
                                    tempo=processedAudioData.origTempo,
                                    key=key,
                                    timeSig=timeSig)

    if not testMode:
        SheetMusicGenerator.generate_midi_file(notes,processedAudioData.tempo,outputName)

    if not testMode:
        Graphing.save_plot(outputName)




    

    duration = time.perf_counter() - startTime
    perSecondOfAudioDuration = duration/processedAudioData.duration

    if CONFIG["ADVANCED_OPTIONS"]["clear_temp"]:
        for file in os.listdir("temp\\"):
            os.remove(f"temp\\{file}")
    
    CUI.newline()
   
    CUI.diagnostic("Processing time per second of audio",round(perSecondOfAudioDuration,3), "seconds")
    CUI.important(f"\nDone. Processing {round(processedAudioData.duration,3)} seconds of audio took {round(duration, 3)} seconds.\n")


    if not testMode:
        Graphing.show_plot()
    return processedMusic
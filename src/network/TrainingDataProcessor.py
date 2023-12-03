import numpy as np
import time
import math
import os

import core.AudioProcessor as AudioProcessor
import core.MIDIManager as MIDIManager
from core.Configurator import CONFIG
import network.SpectrumCompressor as SpectrumCompressor
import cui.CUI  as CUI
from core.Constants import *
import misc.Graphing as Graphing


AUDIO_PATH = "learning\\audio\\"
MIDI_PATH = "learning\\midi\\"

SPECTRA_PATH = "learning\\spectra\\"


ADDED_DELAY = 0.05

def __is_note_playing_at_time(time: float,noteStart: float,noteEnd: float) -> bool:
    return noteStart <= time and noteEnd > time


def process_multiple():
    if not os.path.isdir(f"{SPECTRA_PATH}{CONFIG['ARGS']['audio']}"):
        os.mkdir(f"{SPECTRA_PATH}{CONFIG['ARGS']['audio']}")
    for audioFile in os.listdir(f"{AUDIO_PATH}{CONFIG['ARGS']['audio']}"):


        baseMidiPath = f"{MIDI_PATH}{CONFIG['ARGS']['midi']}\\{audioFile}"[:-4] # Remove .wav or .mp3 from extension
        

        if os.path.isfile(f"{baseMidiPath}.mid"):
            midiPath = f"{baseMidiPath}.mid"

        elif os.path.isfile(f"{baseMidiPath}.midi"):
            midiPath = f"{baseMidiPath}.midi"
        else:
            raise Exception(f"Couldn't find midi file matching {audioFile}")


        __generate(f"{AUDIO_PATH}{CONFIG['ARGS']['audio']}\\{audioFile}",midiPath,f"{SPECTRA_PATH}{CONFIG['ARGS']['audio']}\\{audioFile.split('.')[0]}")


def process_single():
    __generate(f"{AUDIO_PATH}{CONFIG['ARGS']['audio']}",
               f"{MIDI_PATH}{CONFIG['ARGS']['midi']}",
               f"{SPECTRA_PATH}{CONFIG['ARGS']['audio'].split('.')[0]}")


def __generate(audioPath,midiPath,basePath):
    ## Process audio file -> spectrum & onsets
    audioData = AudioProcessor.process_audio(audioPath)

    CUI.progress(f"Getting spectrum",spin=False)

    midi = MIDIManager.get_midi(midiPath)



    uniqueOnsets = []
    for note in midi:
         if note.start not in uniqueOnsets:
              uniqueOnsets.append(note.start + ADDED_DELAY)

    uniqueOnsetCount = len(uniqueOnsets)




    chords = np.zeros((uniqueOnsetCount,NOTE_COUNT),dtype=np.uint8)
    spectrum = np.ndarray((uniqueOnsetCount,SPECTRUM_SIZE))
    Graphing.vLines(uniqueOnsets,0,10,colour="g")

    Graphing.show_plot()
    for i,uniqueOnsetTime in enumerate(uniqueOnsets):
        
        frame = math.ceil(uniqueOnsetTime/audioData.frameDuration) + 2

        spectrum[i] = audioData.spectrum[0:SPECTRUM_SIZE,frame]
        for note in midi:
            if not __is_note_playing_at_time(uniqueOnsetTime,note.start,note.end):
                continue
        
            chords[i,note.pitch - 21] = 1



    start = time.time()
    CUI.progress(f"Compressing",spin=True)

    

    SpectrumCompressor.compress(chords,spectrum,basePath)
    CUI.force_stop_progress()
    
    print(time.time() - start)
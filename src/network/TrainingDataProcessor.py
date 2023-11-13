import numpy as np
import time
import librosa

import AudioProcessor
import MIDIManager
from Configurator import CONFIG
import network.SpectrumCompressor as SpectrumCompressor
import cui.CUI  as CUI
from Constants import *


AUDIO_PATH = "learning\\audio\\"
MIDI_PATH = "learning\\midi\\"





def __is_note_playing_at_time(time: float,noteStart: float,noteEnd: float) -> bool:
    return noteStart <= time and noteEnd > time





def process_training_data():
    ## Process audio file -> spectrum & onsets
    audioData = AudioProcessor.process_audio(f"{AUDIO_PATH}{CONFIG['ARGS']['audio']}")


    CUI.progress(f"Getting spectrum",spin=False)

    midi = MIDIManager.get_midi(f"{MIDI_PATH}{CONFIG['ARGS']['midi']}")

    print(len(midi),len(audioData.onsets))

    #https://stackoverflow.com/questions/7332841/add-single-element-to-array-in-numpy

   

    uniqueOnsets = []
    for note in midi:
         if note.start not in uniqueOnsets:
              uniqueOnsets.append(note.start)

    uniqueOnsetCount = len(uniqueOnsets)

    print(uniqueOnsetCount)


    chords = np.zeros((uniqueOnsetCount,NOTE_COUNT),dtype=np.uint8)
    spectrum = np.ndarray((uniqueOnsetCount,SPECTRUM_SIZE))

    for i,uniqueOnsetTime in enumerate(uniqueOnsets):
        
        frame = AudioProcessor.time_to_frames(uniqueOnsetTime)


        spectrum[i] = audioData.spectrum[0:SPECTRUM_SIZE,frame]
        for note in midi:
            if not __is_note_playing_at_time(uniqueOnsetTime,note.start,note.end):
                continue
        
            chords[i,note.pitch - 21] = 1



    start = time.time()
    CUI.progress(f"Compressing",spin=True)

    fileName = CONFIG['ARGS']['audio'].split(".")[0]

    SpectrumCompressor.compress(chords,spectrum,fileName)
    CUI.force_stop_progress()
    print(time.time() - start)

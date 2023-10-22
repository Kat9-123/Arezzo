import numpy as np
import time
import librosa

import AudioProcessor
import MIDIManager
from Configurator import CONFIG
import network.SpectrumCompressor as SpectrumCompressor



AUDIO_PATH = "learning\\audio\\"
MIDI_PATH = "learning\\midi\\"



INPUT_SIZE = 6222
OUTPUT_SIZE = 88

MAX_ROW = 6222

model = None

def __is_note_playing_at_time(time,noteStart,noteEnd) -> bool:
    return noteStart <= time and noteEnd > time


def __notes_to_one_encoded(notes):
    newNotes = np.zeros(OUTPUT_SIZE,dtype=np.uint8)
    for i in range(0,len(midi)):
        note = midi[i]
        if note[2] - onset > 100:
            break

        if note[1] < onset and note[2] > onset or note[1] == onset:
            newNotes[note[0] - 21] = 1

def process_training_data():
    ## Process audio file -> spectrum & onsets
    audioData = AudioProcessor.process_audio(f"{AUDIO_PATH}{CONFIG['ARGS']['audio']}")


    midi = MIDIManager.get_midi(f"{MIDI_PATH}{CONFIG['ARGS']['midi']}")


    chords = []
    currentlyPlaying = []
    for note in midi:
        time = note.start
        finishedNotes = []


        for playingNote in currentlyPlaying:
            if not __is_note_playing_at_time(time,playingNote.start,playingNote.end):
                finishedNotes.append(playingNote)
                return
            


        for finishedNote in finishedNotes:
            playingNote.remove(finishedNote)


        pass




    print(notes.shape)
    print(spectrum.shape)
    start = time.time()
    print("COMPRESSING")

    fileName = cfg.CONFIG['ARGS']['audio'].split(".")[0]

    SpectrumCompressor.compress(notes,spectrum,fileName)
    print("DONE!")
    print(time.time() - start)

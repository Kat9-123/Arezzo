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





def __is_note_playing_at_time(time,noteStart,noteEnd) -> bool:
    return noteStart <= time and noteEnd > time





def process_training_data():
    ## Process audio file -> spectrum & onsets
    audioData = AudioProcessor.process_audio(f"{AUDIO_PATH}{CONFIG['ARGS']['audio']}")


    CUI.progress(f"Getting spectrum",spin=False)

    midi = MIDIManager.get_midi(f"{MIDI_PATH}{CONFIG['ARGS']['midi']}")

    print(len(midi),len(audioData.onsets))

    onsetCount = len(midi)

    chords = np.zeros((onsetCount,NOTE_COUNT),dtype=np.uint8)
    spectrum = np.ndarray((onsetCount,SPECTRUM_SIZE))


    currentlyPlaying = []
    for i,note in enumerate(midi):
        currentlyPlaying.append(note)


        onsetTime = note.start
        frame = AudioProcessor.time_to_frames(onsetTime)

        spectrum[i] = audioData.spectrum[0:SPECTRUM_SIZE,frame]


        finishedNotes = []

        for playingNote in currentlyPlaying:
            if not __is_note_playing_at_time(onsetTime,playingNote.start,playingNote.end):
                finishedNotes.append(playingNote)
                continue

            chords[i,playingNote.pitch - 21] = 1



        for finishedNote in finishedNotes:
            currentlyPlaying.remove(finishedNote)



    start = time.time()
    CUI.progress(f"Compressing",spin=True)

    fileName = CONFIG['ARGS']['audio'].split(".")[0]

    SpectrumCompressor.compress(chords,spectrum,fileName)
    CUI.force_stop_progress()
    print(time.time() - start)

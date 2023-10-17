import AudioProcessor
import MIDIManager

import numpy as np

import cui.CUI as CUI
import Constants

import network.SpectrumCompressor as SpectrumCompressor

import time


from Configurator import CONFIG


AUDIO_PATH = "learning\\audio\\"
MIDI_PATH = "learning\\midi\\"




model = None

def process_training_data():
    ## Process audio file -> spectrum & onsets
    audioData = AudioProcessor.process_audio(f"{AUDIO_PATH}{CONFIG['ARGS']['audio']}")

    print("                                              TEST")
    CUI.progress(f"Getting spectrum")

   # audioData.tempo = 120
    midi = MIDIManager.get_midi(f"{MIDI_PATH}{CONFIG['ARGS']['midi']}",120)
    tempo = 120
    midiOnsets = []
    earliest = audioData.onsets[0]

    onsetBeats = []



    onsetBeats = []
    for note in midi:
        if note[1] in onsetBeats:
            continue
        onsetBeats.append(note[1])


  #  print(len(uniqueMIDIBeats), len(audioData.onsets))




    notes = np.ndarray((len(onsetBeats),Constants.NOTE_COUNT),dtype=np.uint8)
    spectrum = np.ndarray((len(onsetBeats),Constants.SPECTRUM_SIZE))

    for x,onset in enumerate(onsetBeats):
    

        newNotes = np.zeros(Constants.NOTE_COUNT,dtype=np.uint8)
        for i in range(0,len(midi)):
            note = midi[i]
            if note[2] - onset > 100:
               break

            if note[1] < onset and note[2] > onset or note[1] == onset:
                newNotes[note[0] - 21] = 1


        notes[x] = newNotes



        spectrumOnset = int(onset / ((tempo/60) * audioData.frameDuration) + earliest)

        diff = 10_000
        for i in audioData.onsets:
            d = abs(spectrumOnset - i)
            if d < diff:
                diff = d
        if diff > 1: print(diff)



        spectrum[x] = audioData.spectrum[0:Constants.SPECTRUM_SIZE,spectrumOnset]

    print(notes.shape)
    print(spectrum.shape)
    start = time.time()
    CUI.progress(f"Compressing")

    fileName = CONFIG['ARGS']['audio'].split(".")[0]

    SpectrumCompressor.compress(notes,spectrum,fileName)
    CUI.force_stop_progress()
    print(time.time() - start)

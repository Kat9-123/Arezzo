import AudioProcessor
import MIDIManager
import Utils
import librosa  
import numpy as np
import csv


import torch
from torch import nn

from network.Network import Network
import network.Trainer as Trainer

import network.SpectrumCompressor as SpectrumCompressor
from torch.utils.data import DataLoader
import time
from network.Network import Network
#import network.SpectrumCompressor as SpectrumCompressor
AUDIO_PATH = "learning\\audio\\"
MIDI_PATH = "learning\\midi\\"

FILE_NAME = "mono\\MONO-12-R"

INPUT_SIZE = 6222
OUTPUT_SIZE = 12

MAX_ROW = 6222

model = None

def car():
    ## Process audio file -> spectrum & onsets
    audioData = AudioProcessor.process_audio(f"{AUDIO_PATH}{FILE_NAME}.mp3")


   # audioData.tempo = 120
    midi = MIDIManager.get_midi(f"{MIDI_PATH}{FILE_NAME}.midi",120)
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




    notes = np.ndarray((len(onsetBeats),OUTPUT_SIZE),dtype=np.uint8)
    spectrum = np.ndarray((len(onsetBeats),MAX_ROW))

    for x,onset in enumerate(onsetBeats):


        n = []
        for i in range(0,len(midi)):
            note = midi[i]
            if note[2] - onset > 100:
               break

            if note[1] < onset and note[2] > onset or note[1] == onset:
                n.append(note[0] - 21)



        newNotes = np.zeros(OUTPUT_SIZE,dtype=np.uint8)
        for i in range(OUTPUT_SIZE):
            if i in n:
                newNotes[i] = 1
            else:
                newNotes[i] = 0
        notes[x] = newNotes


        spectrumOnset = int(onset / ((tempo/60) * audioData.frameDuration) + earliest)
        #print(spectrumOnset)

        diff = 10_000
        for i in audioData.onsets:
            d = abs(spectrumOnset - i)
            if d < diff:
                diff = d
        if diff > 1: print(diff)

        row = audioData.spectrum[0:MAX_ROW,spectrumOnset]
        #row = row.round(3)
       # row[row < -40] = -40
       # row = row * -1


        spectrum[x] = row

    print(notes.shape)
    print(spectrum.shape)
    start = time.time()
    print("COMPRESSING")
    SpectrumCompressor.compress(notes,spectrum,FILE_NAME)
    print("DONE!")
    print(time.time() - start)



def setup_trained_model():
    global model
    model = Network() # we do not specify ``weights``, i.e. create untrained model
    model.load_state_dict(torch.load('network.mdl'))
    model.eval()

    

def get_model_output(data):
    data = torch.tensor(data,dtype=torch.float32)
    output = model(data)
    pred = (output > 0.5).float()
    return pred
    #prediction = torch.argmax(output)
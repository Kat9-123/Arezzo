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

from network.Dataset import Dataset
from torch.utils.data import DataLoader
AUDIO_PATH = "data\\BACH.wav"
MIDI_PATH = "data\\BACH.mid"


def train():

    ## Process audio file -> spectrum & onsets
    audioData = AudioProcessor.process_audio(AUDIO_PATH)


   # audioData.tempo = 120
    midi = MIDIManager.get_midi(MIDI_PATH,120)
    tempo = 120
    midiOnsets = []
    earliest = audioData.onsets[0]
    for onset in audioData.onsets:
        
        midiOnsets.append(Utils.snap_to_beat((onset - earliest) * (tempo/60) * audioData.frameDuration))

    for note in midi:
        print(note)

    data = []
    for x,onset in enumerate(midiOnsets):
        newRow = list(audioData.spectrum[:,audioData.onsets[x]])
        notesAtOnset = []
        for note in midi:
            # 0 1
            
            if note[1] < onset and note[2] > onset or note[1] == onset:

                notesAtOnset.append(librosa.note_to_midi(note[0]) - 21) # A0 = 0, C8 = 87


        for i in range(88):
            if i not in notesAtOnset:
                newRow.append(0)
                continue
        
            newRow.append(1)

        

        data.append(newRow)


    print(data[0][1025])
    print(len(data[0]))
    print(len(data[22]))
    input()

    with open("BACH.csv","w") as f:
        write = csv.writer(f)
        write.writerows(data)

    """



    labels = notes
    testLabels = labels[-20:]
    testOnsets = labels[-20:]

    trainingData = Dataset(labels,audioData.onsets,audioData.spectrum)
    testData = Dataset(testLabels,testOnsets,audioData.spectrum)

    trainingLoader = DataLoader(trainingData,batch_size=32,shuffle=True)
    testLoader = DataLoader(testData,batch_size=32,shuffle=True)
                
    model = Network(audioData.spectrum.shape[0]).to("cpu")
    print(model)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    epochs = 5
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        Trainer.train(trainingLoader, model, loss_fn, optimizer)
        Trainer.test(testLoader, model, loss_fn)
    print("Done!")
    
    """

    


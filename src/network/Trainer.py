# Adapted from https://machinelearningmastery.com/building-a-multiclass-classification-model-in-pytorch/
import copy

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import tqdm
from sklearn.model_selection import train_test_split

from network.Network import Network
import network.SpectrumCompressor as SpectrumCompressor
from Configurator import CONFIG
#import SpectrumCompressor
import Constants





TRAIN_TEST_PERCENTAGE = 0.7



EPOCH_COUNT = 100
BATCH_SIZE = 5
NOISE_DEVIATION = 3.5

DEVICE = CONFIG["ADVANCED_OPTIONS"]["training_device"]



def __accuracy(output, target) -> float:
    pred = (output > 0.5).float()

    maxScore = target.sum()
    score = maxScore

    mistakes = (pred != target).sum()


    return (score - mistakes)/maxScore
    

def __save_model(model,dataPath) -> None:
    if not CONFIG["DEBUG"]['save_model']:
        return

    netPath = dataPath.split(".")[0] + ".mdl"
    torch.save(model.state_dict(), netPath)



def __eval_debug_samples(model,spectra,notes):
    for i in range(20):
        out = model(spectra[i].to(DEVICE))
        for x in range(len(out)):
            if out[x] > 0.5:
                print(x)
        print("TARGET")

        for x in range(len(notes[i])):
            if notes[i][x] > 0.5:
                print(x)
        
        print(__accuracy(out,notes[i].to(DEVICE)))




def __generate_noise(batchSize):
    
    return (torch.rand((batchSize,Constants.SPECTRUM_SIZE)) * (NOISE_DEVIATION*2)) - NOISE_DEVIATION







def train():
    dataPath = CONFIG["ARGS"]['training_data']

    notes,spectrum = SpectrumCompressor.decompress(dataPath)




    spectrum = torch.tensor(spectrum, dtype=torch.float32)
    notes = torch.tensor(notes, dtype=torch.float32)

    # split
    spectrumTrain, spectrumTest, notesTrain, notesTest = train_test_split(spectrum, notes, train_size=TRAIN_TEST_PERCENTAGE, shuffle=True)






    model = Network().to(DEVICE)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.SGD(model.parameters(), lr=1e-3)




    batchesPerEpoch = len(spectrumTrain) // BATCH_SIZE

    bestAccuracy = -np.inf
    bestWeights = None

    trainLossHist = []
    trainAccuracyHist = []
    testLossHist = []
    testAccuracyHist = []




    # training loop
    for epoch in range(EPOCH_COUNT):
        epochLoss = []
        epochAccuracy = []
        # set model in training mode and run through each batch
        model.train()
        with tqdm.trange(batchesPerEpoch, unit="batch", mininterval=0) as bar:
            bar.set_description(f"Epoch {epoch}")
            for i in bar:

                # Get batch                
                start = i * BATCH_SIZE
                spectrumBatch = spectrumTrain[start:start+BATCH_SIZE]
                noteBatch = notesTrain[start:start+BATCH_SIZE]


                # Add some noise to help prevent overfitting, and to hopefully give better results
                noise = __generate_noise(BATCH_SIZE)

                # Forward
                prediction = model((spectrumBatch + noise).to(DEVICE))

                # Derivatives
                loss = criterion(prediction.to(DEVICE), noteBatch.to(DEVICE))

                # Backward
                optimizer.zero_grad()
                loss.backward()

                optimizer.step()

                # compute and store metrics
                accuracy = __accuracy(prediction,noteBatch.to(DEVICE))


                epochLoss.append(float(loss))
                epochAccuracy.append(float(accuracy))
                bar.set_postfix(
                    loss=float(loss),
                    acc=float(accuracy)
                )

        # Set model in evaluation mode and run through the test set
        model.eval()
        prediction = model(spectrumTest.to(DEVICE))
        crossEntropy = criterion(prediction.to(DEVICE), notesTest.to(DEVICE))

        accuracy = __accuracy(prediction,notesTest.to(DEVICE))
        crossEntropy = float(crossEntropy)
        accuracy = float(accuracy)

        trainLossHist.append(np.mean(epochLoss))
        trainAccuracyHist.append(np.mean(epochAccuracy))
        testLossHist.append(crossEntropy)
        testAccuracyHist.append(accuracy)

        if accuracy > bestAccuracy:
            bestAccuracy = accuracy
            bestWeights = copy.deepcopy(model.state_dict())

        print(f"Epoch {epoch} validation: Cross-entropy={crossEntropy:.2f}, Accuracy={accuracy*100:.1f}%")

    # Restore best model
    model.load_state_dict(bestWeights)

    __save_model(model,dataPath)

    model.eval()


    __eval_debug_samples(model,spectrum,notes)


    # Plot the loss and accuracy
    plt.plot(trainLossHist, label="train")
    plt.plot(testLossHist, label="test")
    plt.xlabel("epochs")
    plt.ylabel("cross entropy")
    plt.legend()
    plt.show()

    plt.plot(trainAccuracyHist, label="train")
    plt.plot(testAccuracyHist, label="test")
    plt.xlabel("epochs")
    plt.ylabel("accuracy")
    plt.legend()
    plt.show()
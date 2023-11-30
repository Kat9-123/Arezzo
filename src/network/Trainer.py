# Adapted from https://machinelearningmastery.com/building-a-multiclass-classification-model-in-pytorch/
import copy

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import tqdm

from network.Network import Network

from Configurator import CONFIG
#import SpectrumCompressor
import Constants
import Utils
from network.Dataset import SpectrumDataset





TRAIN_TEST_PERCENTAGE = 0.7



EPOCH_COUNT = 60
BATCH_SIZE = 5
NOISE_DEVIATION = 3.5



DEVICE = "cpu"
if torch.cuda.is_available() and CONFIG["ADVANCED_OPTIONS"]["use_cuda_if_available"]:
    DEVICE = "cuda"


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


    path = Utils.generate_filepath_handle_duplicates(netPath)
    torch.save(model.state_dict(), path)



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


    dataset = SpectrumDataset(dataPath)

    trainSet, testSet = torch.utils.data.random_split(dataset, [TRAIN_TEST_PERCENTAGE, 1-TRAIN_TEST_PERCENTAGE])

    # Creating data indices for training and validation splits:
    train_loader = torch.utils.data.DataLoader(trainSet, batch_size=BATCH_SIZE, 
                                            shuffle=True)
    validation_loader = torch.utils.data.DataLoader(testSet, batch_size=BATCH_SIZE,
                                                    shuffle=True)







    model = Network().to(DEVICE)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.SGD(model.parameters(), lr=1e-3)




    batchesPerEpoch = len(train_loader)

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

            for i, (spectrumBatch, noteBatch) in enumerate(train_loader):



                # Add some noise to help prevent overfitting, and to hopefully give better results
                noise = __generate_noise(len(spectrumBatch))

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
                bar.update()
        # Set model in evaluation mode and run through the test set
        model.eval()
        testAccuracy = []
        for spectrum,note in validation_loader:

            prediction = model(spectrum.to(DEVICE))
            crossEntropy = criterion(prediction.to(DEVICE), note.to(DEVICE))

            batchAccuracy = __accuracy(prediction,note.to(DEVICE))
            crossEntropy = float(crossEntropy)
            batchAccuracy = float(batchAccuracy)

            testAccuracy.append(batchAccuracy)


        accuracy = np.mean(testAccuracy)
        trainLossHist.append(np.mean(epochLoss))
        trainAccuracyHist.append(np.mean(epochAccuracy))
       # testLossHist.append(crossEntropy)
        #testAccuracyHist.append(accuracy)

        if accuracy > bestAccuracy:
            bestAccuracy = accuracy
            bestWeights = copy.deepcopy(model.state_dict())

        print(f"Epoch {epoch} validation: Cross-entropy={crossEntropy:.2f}, Accuracy={accuracy*100:.1f}%")

    # Restore best model
    model.load_state_dict(bestWeights)

    __save_model(model,dataPath)

    model.eval()


    #__eval_debug_samples(model,spectrum,notes)


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
# Adapted from https://machinelearningmastery.com/building-a-multiclass-classification-model-in-pytorch/
import copy

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import tqdm
import datetime
import time


from network.Network import Network

from core.Configurator import CONFIG
#import SpectrumCompressor
import core.Constants as Constants
import core.Utils as Utils
from network.Dataset import SpectrumDataset
import cui.CUI as CUI




TRAIN_VALIDATION_TEST_SPLIT = [0.65,0.3,0.05]
SUBSET_SPLIT = [0.13,0.06,0.01,0.8]


EPOCH_COUNT = 10000
BATCH_SIZE = 10
NOISE_DEVIATION = 2.5



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

    print(f"Saving model to {path}")
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




def __eval_model(loader,model,criterion):

    model.eval()
    batchCount = len(loader)
    accuracies = np.zeros(batchCount)
    losses = np.zeros(batchCount)

    for i, (spectrum,note) in enumerate(loader):

        prediction = model(spectrum.to(DEVICE))
        batchLoss = criterion(prediction.to(DEVICE), note.to(DEVICE))

        batchAccuracy = __accuracy(prediction,note.to(DEVICE))

        batchLoss = float(batchLoss)
        batchAccuracy = float(batchAccuracy)

        accuracies[i] = batchAccuracy
        losses[i] = batchLoss
    
    return np.mean(accuracies), np.mean(losses)


def train():
    dataPath = CONFIG["ARGS"]['training_data']


    dataset = SpectrumDataset(dataPath,DEVICE)

    trainDataset, validationDataset, testDataset = torch.utils.data.random_split(dataset, TRAIN_VALIDATION_TEST_SPLIT)

    # Creating data indices for training and validation splits:
    trainLoader = torch.utils.data.DataLoader(trainDataset, batch_size=BATCH_SIZE, 
                                                    shuffle=True)
    validationLoader = torch.utils.data.DataLoader(validationDataset, batch_size=BATCH_SIZE,
                                                   shuffle=True)

    testLoader = torch.utils.data.DataLoader(testDataset, batch_size=BATCH_SIZE,
                                                    shuffle=True)





    model = Network().to(DEVICE)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.SGD(model.parameters(), lr=1e-3)




    batchesPerEpoch = len(trainLoader)

    bestAccuracy = -np.inf
    bestWeights = None

    trainLossHist = []
    trainAccuracyHist = []
    validationLossHist = []
    validationAccuracyHist = []

    CUI.diagnostic("Dataset size",len(dataset))
    CUI.diagnostic("Batch size",BATCH_SIZE)

    CUI.diagnostic("Training size",len(trainLoader)*BATCH_SIZE)
    CUI.diagnostic("Validation size",len(validationLoader)*BATCH_SIZE)
    CUI.diagnostic("Test size",len(testLoader)*BATCH_SIZE)

    CUI.progress("Training...")

    # training loop
    startTime = time.time()
    previousAccuracy = 0.0
    for epoch in range(EPOCH_COUNT):
        try:

            trainLoss = np.zeros(batchesPerEpoch)
            trainAccuracy = np.zeros(batchesPerEpoch)
            # set model in training mode and run through each batch
            model.train()
            with tqdm.trange(batchesPerEpoch, unit="batch", mininterval=0,ascii=True) as bar:
                bar.set_description(f"Epoch {epoch}")

                for i,(spectrumBatch, noteBatch) in enumerate(trainLoader):



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


                    trainLoss[i] = float(loss)
                    trainAccuracy[i] = float(accuracy)
                    bar.set_postfix(
                        loss=f"{float(loss):5.2f}",
                        acc=f"{float(accuracy):5.2f}",
                    )
                    bar.update()
            # Set model in evaluation mode and run through the validation set
            print("Validating...",end="\r")
            avgTrainLoss = np.mean(trainLoss)
            avgTrainAccuracy = np.mean(trainAccuracy)


            trainLossHist.append(avgTrainLoss)
            trainAccuracyHist.append(avgTrainAccuracy)



            validationAccuracy,validationLoss = __eval_model(validationLoader,model,criterion)






            validationLossHist.append(validationLoss)
            validationAccuracyHist.append(validationAccuracy)

            if validationAccuracy > bestAccuracy:
                bestAccuracy = validationAccuracy
                bestWeights = copy.deepcopy(model.state_dict())



            print(f"Epoch {epoch}              ")
            print(f"     Train - Loss: {avgTrainLoss:.2f}, Accuracy: {avgTrainAccuracy*100:.1f}%")
            print(f"Validation - Loss: {validationLoss:.2f}, Accuracy: {validationAccuracy*100:.1f}%")
            print(f"ΔAccuracy: {(validationAccuracy-previousAccuracy)*100:.1f} Train-Validation diff: {(avgTrainAccuracy-validationAccuracy)*100:.1f}")
            
            timeSpent = round(time.time()-startTime)

            print(f"Time spent: {str(datetime.timedelta(seconds=timeSpent))}, Time per epoch: {str(datetime.timedelta(seconds=round(timeSpent/(epoch+1))))}")
            print()
            previousAccuracy = validationAccuracy

        except KeyboardInterrupt:
            print("Stopping training...")
            break
    
    if bestWeights == None:
        CUI.warning("At least one epoch has to finish for results!")
        input()
        exit()

    # Restore best model
    model.load_state_dict(bestWeights)

    __save_model(model,dataPath)

    testAccuracy, testLoss = __eval_model(testLoader,model,criterion)
    print(f"Test - Loss: {testLoss:.2f}, Accuracy: {testAccuracy*100:.1f}%")


    #__eval_debug_samples(model,spectrum,notes)


    # Plot the loss and accuracy
    plt.plot(trainLossHist, label="train")
    plt.plot(validationLossHist, label="validation")
    plt.axhline(y = testLoss, color = 'r', linestyle = 'dashed',label="test")  
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()

    plt.plot(trainAccuracyHist, label="train")
    plt.plot(validationAccuracyHist, label="validation")
    plt.axhline(y = testAccuracy, color = 'r', linestyle = 'dashed',label="test")  
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.show()
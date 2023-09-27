import copy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import tqdm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from network.Network import Network
import network.SpectrumCompressor as SpectrumCompressor
import Config as cfg
#import SpectrumCompressor

DEVICE = "cuda"

INPUT_SIZE = 6222
OUTPUT_SIZE = 88



def __accuracy(output, target):
    pred = (output > 0.5).float()

    maxScore = target.sum()
    score = maxScore

    mistakes = (pred != target).sum()


    return (score - mistakes)/maxScore
    

def train():

    notes,spectrum = SpectrumCompressor.decompress(cfg.CONFIG['NETWORK']['training_data'])



    X = spectrum
    y = notes


    # convert pandas DataFrame (X) and numpy array (y) into PyTorch tensors
    X = torch.tensor(X, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.float32)

    # split
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, shuffle=True)





    # loss metric and optimizer
    model = Network().to(DEVICE)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.SGD(model.parameters(), lr=1e-3)
    #optimizer = optim.Adam(model.parameters(), lr=1e-3)

    # prepare model and training parameters
    n_epochs = 500
    batch_size = 5
    batches_per_epoch = len(X_train) // batch_size

    best_acc = - np.inf   # init to negative infinity
    best_weights = None
    train_loss_hist = []
    train_acc_hist = []
    test_loss_hist = []
    test_acc_hist = []




    # training loop
    for epoch in range(n_epochs):
        epoch_loss = []
        epoch_acc = []
        # set model in training mode and run through each batch
        model.train()
        with tqdm.trange(batches_per_epoch, unit="batch", mininterval=0) as bar:
            bar.set_description(f"Epoch {epoch}")
            for i in bar:
                # take a batch
                
                start = i * batch_size
                X_batch = X_train[start:start+batch_size]
                y_batch = y_train[start:start+batch_size]
                # forward pass
                y_pred = model(X_batch.to(DEVICE))
                loss = criterion(y_pred.to(DEVICE), y_batch.to(DEVICE))
                # backward pass
                optimizer.zero_grad()
                loss.backward()
                # update weights
                optimizer.step()
                # compute and store metrics
                acc = __accuracy(y_pred,y_batch.to(DEVICE))
                #acc = (torch.argmax(y_pred, 1) == torch.argmax(y_batch.to(DEVICE), 1)).float().mean()
                epoch_loss.append(float(loss))
                epoch_acc.append(float(acc))
                bar.set_postfix(
                    loss=float(loss),
                    acc=float(acc)
                )
        # set model in evaluation mode and run through the test set
        model.eval()
        y_pred = model(X_test.to(DEVICE))
        ce = criterion(y_pred.to(DEVICE), y_test.to(DEVICE))
        #acc = (torch.argmax(y_pred, 1) == torch.argmax(y_test.to(DEVICE), 1)).float().mean()
        acc = __accuracy(y_pred,y_test.to(DEVICE))
        ce = float(ce)
        acc = float(acc)
        train_loss_hist.append(np.mean(epoch_loss))
        train_acc_hist.append(np.mean(epoch_acc))
        test_loss_hist.append(ce)
        test_acc_hist.append(acc)
        if acc > best_acc:
            best_acc = acc
            best_weights = copy.deepcopy(model.state_dict())
        print(f"Epoch {epoch} validation: Cross-entropy={ce:.2f}, Accuracy={acc*100:.1f}%")

    # Restore best model
    model.load_state_dict(best_weights)

    if cfg.CONFIG['NETWORK']['save_model']:
        torch.save(model.state_dict(), 'network.mdl')

    model.eval()


    for i in range(20):
        out = model(X[i].to(DEVICE))
        for x in range(len(out)):
            if out[x] > 0.5:
                print(x)
        print("TARGET")
        for x in range(len(y[i])):
            if y[i][x] > 0.5:
                print(x)
        
        print(__accuracy(out,y[i].to(DEVICE)))


    # Plot the loss and accuracy
    plt.plot(train_loss_hist, label="train")
    plt.plot(test_loss_hist, label="test")
    plt.xlabel("epochs")
    plt.ylabel("cross entropy")
    plt.legend()
    plt.show()

    plt.plot(train_acc_hist, label="train")
    plt.plot(test_acc_hist, label="test")
    plt.xlabel("epochs")
    plt.ylabel("accuracy")
    plt.legend()
    plt.show()
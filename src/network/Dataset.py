from torch.utils.data import Dataset
import numpy as np
import pandas as pd
class Dataset(Dataset):

    def __init__(self, labels, onsets, spectrum, transform=None, target_transform=None):
        self.spectrum = spectrum
        self.onsets = onsets
        self.labels = pd.DataFrame(labels)
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):

        slice = self.spectrum[:,self.onsets[idx]]
        label = self.labels.iloc[idx,0]
        if self.transform:
            slice = self.transform(slice)
        if self.target_transform:
            label = self.target_transform(label)
        return slice, label
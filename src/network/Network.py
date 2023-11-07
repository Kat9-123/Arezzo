import os
from torch import nn
from torch.utils.data import DataLoader
import Constants


class Network(nn.Module):

 
    def __init__(self):
        super().__init__()
        

        self.relu_stack = nn.Sequential(
            nn.Linear(Constants.SPECTRUM_SIZE, 1000),
            nn.ReLU(),
           # nn.Linear(1000,500),
          #  nn.ReLU(),
            nn.Linear(1000, Constants.NOTE_COUNT)
        )

        
    def forward(self, x):
        logits = self.relu_stack(x)
        return logits
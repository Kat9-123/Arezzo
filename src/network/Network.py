import os
from torch import nn
from torch.utils.data import DataLoader


class Network(nn.Module):

 
    def __init__(self):
        super().__init__()
        

        self.relu_stack = nn.Sequential(
            nn.Linear(6222, 1000),
            nn.ReLU(),
            nn.Linear(1000, 88)
        )

        
    def forward(self, x):
        logits = self.relu_stack(x)
        return logits
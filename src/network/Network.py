import os
from torch import nn
from torch.utils.data import DataLoader



class Network(nn.Module):
    def __init__(self,size):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(size,1024),
            nn.ReLU(),
            nn.Linear(1024,1024),
            nn.ReLU(),
            nn.Linear(1024,88)

        )

    def forward(self,x):
       # x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits
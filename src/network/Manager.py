

import torch
from network.Network import Network
from network.Network import Network

model = None




def setup_trained_model():
    global model
    model = Network() 
    model.load_state_dict(torch.load('network.mdl',map_location=torch.device("cpu")))
    model.eval()

    

def get_model_output(data):
    data = torch.tensor(data,dtype=torch.float32)
    output = model(data)
    #print(torch.round(output,decimals=1).tolist())
    pred = (output > 0.5).float()
    return pred
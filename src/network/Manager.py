

import torch
from network.Network import Network
from network.Network import Network
import Configurator as cfg

model = None




def setup_trained_model():
    global model
    model = Network() 
    model.load_state_dict(torch.load(cfg.CONFIG["ADVANCED_OPTIONS"]["model"],map_location=torch.device("cpu")))
    model.eval()

    

def get_model_output(data):
    data = torch.tensor(data,dtype=torch.float32)
    output = model(data)
    print(output)
    #print(torch.round(output,decimals=1).tolist())
    pred = (output > 0.5).float()
    return pred
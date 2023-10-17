

import torch
from network.Network import Network
from Configurator import CONFIG

model = None




def setup_trained_model():
    global model
    model = Network() 
    model.load_state_dict(torch.load(CONFIG["ADVANCED_OPTIONS"]["model"],
                                     map_location=torch.device(CONFIG["ADVANCED_OPTIONS"]["training_device"])))
    model.eval()

    

def get_model_output(data):
    data = torch.tensor(data,dtype=torch.float32)
    output = model(data)
    print(output)
    #print(torch.round(output,decimals=1).tolist())
    pred = (output > 0.5).float()
    return pred
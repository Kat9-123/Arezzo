
import torch
from network.Network import Network
from core.Configurator import CONFIG

model = None


USAGE_DEVICE = "cpu"


def setup_trained_model():
    global model
    model = Network() 
    model.load_state_dict(torch.load(f'models\\{CONFIG["ADVANCED_OPTIONS"]["model"]}',map_location=torch.device(USAGE_DEVICE)))
    model.eval()

    

def get_model_output(data):
    data = torch.tensor(data,dtype=torch.float32)
    output = model(data)
    #print(output)
    #print(torch.round(output,decimals=1).tolist())
    pred = (output > CONFIG["ADVANCED_OPTIONS"]["note_detection_threshold"]).float()
    return pred
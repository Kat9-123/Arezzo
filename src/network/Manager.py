from core.Configurator import CONFIG
from network.Network import Network

import torch




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

    pred = (output > CONFIG["OPTIONS"]["note_detection_threshold"]).float()
    return pred
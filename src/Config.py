import argparse


import tomli


CONFIG_FILE = "cfg.toml"


CONFIG = {}

def __parse_args():
    parser = argparse.ArgumentParser(description='Automatic polyphonic piano transcription in Python.')

    parser.add_argument('path', type=str,
                    help='Path of the file to be processed', nargs='?',default="")
    

    parser.add_argument('-cfg', '--config', type=str,
                    help=f"Path to a ---.toml file. Default is {CONFIG_FILE}",default=CONFIG_FILE) 

    return(parser.parse_args())




def get_configuration():
    global CONFIG

    args = __parse_args()
    CONFIG = __parse_config_file(args.config)
    


    if args.path == "" and CONFIG["path"] == "":
        raise Exception("No file found. Please pass a file path as argument, or fill the path field in cfg.toml")
    
    if CONFIG["path"] == "":
        CONFIG["path"] = args.path



def __parse_config_file(configFilePath) -> dict:
    with open(configFilePath, "rb") as f:
       return(tomli.load(f))

    
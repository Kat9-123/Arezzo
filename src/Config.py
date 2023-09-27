import argparse


import tomli


CONFIG_FILE = "cfg.toml"


CONFIG = {}


# MODES:
# Default
# Test
# Train
# Process
def __parse_args():
    parser = argparse.ArgumentParser(description='Automatic polyphonic piano music transcription in Python.')

    parser.add_argument('path', type=str,
                    help='Path of the AUDIO file to be processed', nargs='?',default="")
    

    parser.add_argument('--cfg','--config', type=str,
                    help=f"Path to a ---.toml file. Default is {CONFIG_FILE}",
                    dest="config", default=CONFIG_FILE,metavar="CONFIG")
    

    
    parser.add_argument("--test", dest="test",type=str,metavar=".MIDI/.CSV",
                        help="""Activates test mode. If a MIDI file is passed, 
                        it will compare the result of the given audio file against that.
                        If a CSV is passed, it will use the files specified. 
                        If no arg is passed it will default to tests.csv""")

    parser.add_argument("--ptd","--process-training-data",type=str,metavar=".MIDI",
                        
                        help="Processes the given audio file combined with the given midi file. Generates: [AUDIO_NAME].csd ")
    
    parser.add_argument("--train",type=str, metavar=".CSD",
                    
                    help="Start training the network on the given .csd file")

    return(parser.parse_args())








def __parse_config_file(configFilePath) -> dict:

    with open(configFilePath, "rb") as f:
       return(tomli.load(f))


def get_configuration() -> None:
    """Load configuration from the default file if not specified by --cfg. 
    Config info gets overriden by args."""
    global CONFIG

    args = __parse_args()

    CONFIG = __parse_config_file(args.config)
    


    if args.path == "" and CONFIG["path"] == "":
        raise Exception("No file found. Please pass a file path as argument, or fill the path field in cfg.toml")

    if args.test:
        CONFIG["testing"] = True

    if CONFIG["path"] == "":
        CONFIG["path"] = args.path
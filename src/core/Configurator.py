import argparse
from enum import Enum
import tomli
import cui.CUI as CUI


CONFIG_FILE = "config.toml"
TESTS = "testing\\tests.csv"


CONFIG = {}

mode = -1

class Modes(Enum):
    GENERATE_SHEETMUSIC = 0
    PROCESS_TRAINING_DATA = 1
    PROCESS_MULTIPLE_TRAINING_DATA = 2
    TRAIN = 3
    TEST = 4
    

def __parse_args():
    parser = argparse.ArgumentParser(prog="Arezzo",description='Arezzo: Automatic polyphonic piano music transcription in Python.',
                                     epilog=f"For more advanced options, please see {CONFIG_FILE}")

    parser.add_argument('path', type=str,
                    help='Path of the AUDIO file to be processed.', nargs='?',default="")
    

    parser.add_argument("-c",'--cfg','--config', type=str,
                    help=f"Path to a .toml file. Default is {CONFIG_FILE}",
                    dest="config", default=CONFIG_FILE,metavar="CONFIG")
    
    parser.add_argument("-n","--net","--network",dest="network",type=str,metavar=".MIDI/.CSD/DIR",
                        
                        help="""If a .csd file is passed, it will train the network on that. Otherwise it will
                        generate a new .csd using the audio and midi file specified. You can also pass a folder containing only MIDI files, 
                        matching audio files will be found automatically in the specified audio folder""")
    
    parser.add_argument("-t","--test", dest="test",type=str,metavar=".MIDI/.CSV",const=TESTS,
                        help=f"""Activates test mode. If a CSV is passed, it will use that. 
                        If no arg is passed it will default to {TESTS}""",nargs="?")

    parser.add_argument("-m","--model",dest="model",type=str,metavar=".MDL",
                        
                        help="""Specify the model to be used when processing the audio""")
    
    parser.add_argument("-o", "--outtype",dest="outFileType",type=str,metavar=".PDF/.PNG/.MIDI",default=".pdf",
                        help="""Specify output file type.""")
    


    return(parser.parse_args())








def __parse_config_file(configFilePath) -> dict:

    with open(configFilePath, "rb") as f:
       return(tomli.load(f))


def get_configuration() -> None:
    """Load configuration from the default file if not specified by --cfg. 
    Config info gets overriden by args."""
    global CONFIG, mode

    args = __parse_args()

    CONFIG = __parse_config_file(args.config)
    CONFIG["ARGS"] = {}

    CONFIG["ARGS"]["audio"] = args.path

    CONFIG["ARGS"]["out_type"] = args.outFileType



    if args.network:
        s = args.network.lower()
        if s.endswith(".csd") or (CONFIG["ARGS"]["audio"] == "" and '.' not in s):
            CONFIG["ARGS"]["training_data"] = args.network
            mode = Modes.TRAIN

        elif s.endswith(".mid") or s.endswith(".midi"):
            CONFIG["ARGS"]["midi"] = args.network
            mode = Modes.PROCESS_TRAINING_DATA
            if CONFIG["ARGS"]["audio"] == "" or CONFIG["ARGS"]["audio"].endswith(".mid") or CONFIG["ARGS"]["audio"].endswith(".midi"):
                CUI.force_stop_progress(succesful=False)
                raise Exception("Invalid usage. Please pass the audio file or folder BEFORE the network argument")
        elif '.' not in s:
            mode = Modes.PROCESS_MULTIPLE_TRAINING_DATA
            CONFIG["ARGS"]["midi"] = args.network


    elif args.test:
        s = args.test.lower()
        mode = Modes.TEST
        if s.endswith(".csv"):
            CONFIG["ARGS"]["test"] = args.test
        else:
            CONFIG["ARGS"]["test"] = TESTS

    else:
        if args.path == "":
            CUI.force_stop_progress(succesful=False)
            raise Exception("Invalid usage. To transcribe please pass an audio file as an argument or drag it onto Arezzo.exe/.bat. For other options use -h or --help")
        

        mode = Modes.GENERATE_SHEETMUSIC

    if args.model:
        CONFIG["ADVANCED_OPTIONS"]["model"] = args.model
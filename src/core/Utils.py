import os
import cui.CUI as CUI
from core.Configurator import CONFIG
from subprocess import Popen

def sys_call(command: str) -> None:
    """System call wrapper with diagnostic print."""
    CUI.print_colour(f"SYSTEM CALL: '{command}'", CUI.PURPLE, end="\n")
    Popen(command, shell=True).wait()



def generate_filepath_handle_duplicates(basePath: str) -> str:

    baseName, extension = basePath.split('.')
    path = basePath
    i = 0

    while os.path.isfile(path):
        i += 1
        path = f"{baseName} ({i}).{extension}"

    return path





def snap_to_beat(time: float) -> float:
    """Takes a rough estimate for beat alignment, and snaps it to the beat."""
    time += CONFIG["ADVANCED_OPTIONS"]["onset_to_beat_lag"]

    
    noteDepth = 2**CONFIG["OPTIONS"]["note_depth"]

    result = time * noteDepth
    result = round(result)
    result /= noteDepth

    return float(result)

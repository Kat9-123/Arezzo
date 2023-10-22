import os
import cui.CUI as CUI
from Configurator import CONFIG
from subprocess import Popen

def sys_call(command: str) -> None:
    """System call wrapper with diagnostic print."""
    CUI.print_colour(f"SYSTEM CALL: '{command}'", CUI.PURPLE, end="\n")
    Popen(command, shell=True).wait()






def snap_to_beat(time: float) -> float:
    """Takes a rough estimate for beat alignment, and snaps it to the beat."""
    #time += cfg.CONFIG["OPTIONS"]["time_to_beat_lag"]

    
    noteDepth = 2**CONFIG["OPTIONS"]["note_depth"]

    result = time * noteDepth
    result = round(result)
    result /= noteDepth

    return float(result)
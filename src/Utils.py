import os
import cui.CUI as CUI
import Configurator as cfg


def sys_call(command: str) -> None:
    """System call wrapper with diagnostic print."""
    CUI.print_colour(f"SYSTEM CALL: '{command}'", CUI.PURPLE, end="\n")
    os.system(command)






def snap_to_beat(time: float) -> float:
    """Takes a rough estimate for beat alignment, and snaps it to the beat."""
    #time += cfg.CONFIG["OPTIONS"]["time_to_beat_lag"]
    if time == 0.0:
        #UI.warning("Zero Time")
        return 0.0
    
    noteDepth = 2**cfg.CONFIG["OPTIONS"]["note_depth_power"]

    result = time * noteDepth
    result = round(result)
    result /= noteDepth

    return float(result)
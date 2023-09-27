import os
import ui.UI as UI
import Config as cfg


def sys_call(command: str) -> None:
    """System call wrapper with diagnostic print."""
    UI.print_colour(f"SYSTEM CALL: '{command}'", UI.PURPLE, end="\n")
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
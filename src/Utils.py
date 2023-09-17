import os
import ui.UI as UI
import Config as cfg


def sys_call(command: str) -> None:
    """System call wrapper with diagnostic print."""
    UI.print_colour(f"SYSTEM CALL: '{command}'", UI.PURPLE, end="\n")
    os.system(command)



# 2 -> Semiquavers
# 3 -> Demisemiquavers
# etc.


def snap_to_beat(time: float) -> float:
    """Takes a rough estimate for beat alignment, and snaps it to the beat."""

    if time == 0.0:
        #UI.warning("Zero Time")
        return 0.0
    
    noteDepth = cfg.CONFIG["OPTIONS"]["note_depth"]

    result = time * noteDepth
    result = round(result)
    result /= noteDepth

    return float(result)
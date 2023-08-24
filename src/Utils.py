import os
import ui.UI as UI


def sys_call(command: str) -> None:
    """System call wrapper with diagnostic print"""
    UI.print_colour(f"SYSTEM CALL: '{command}'", UI.PURPLE, end="\n")
    os.system(command)



# 2 -> Semiquavers
# 3 -> Demisemiquavers
# etc.
NOTE_DEPTH = 2**2

def snap_to_beat(time):


    if time == 0.0:
        #UI.warning("Zero Time")
        return 0.0
    
    result =  time * NOTE_DEPTH

    result = round(result)

    result /= NOTE_DEPTH


    #print(time, "=>", result)
    return float(result)
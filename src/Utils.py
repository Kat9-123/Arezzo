import os
import ui.UI as UI


def sys_call(command: str) -> None:
    UI.print_colour(f"SYSTEM CALL: '{command}'", UI.PURPLE, end="\n")
    os.system(command)


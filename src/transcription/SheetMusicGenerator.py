import cui.CUI as CUI
import core.Utils as Utils
from core.Configurator import CONFIG
import core.MIDIManager as MIDIManager
import os
from pathlib import Path



def __clear_temp():
    if not CONFIG["ADVANCED_OPTIONS"]["clear_temp"]:
        return
    for file in os.listdir("temp\\"):
        os.remove(f"temp\\{file}")


def __confirm_temp_exists():
    if not os.path.isdir("temp\\"):
        os.mkdir("temp\\")

def generate_sheet_music(notes,tempo,outputName) -> None:
    """Takes a list of note objects, and a tempo and creates a MIDI file."""

    if not CONFIG["DEBUG"]["generate_sheet_music"]:
        return
    

    CUI.progress("Generating sheet music")

    __confirm_temp_exists()


    if not CONFIG["ADVANCED_OPTIONS"]["output_cleanly"]:
        midiPath = f"output\\midi\\{outputName}.mid"
    else:
        midiPath = f"temp\\{outputName}.mid"

    MIDIManager.write_midi(notes,tempo,midiPath)

    CUI.diagnostic("MIDI",midiPath)



    succesful = __generate_sheetmusic_musescore(midiPath,outputName)


    __clear_temp()


    CUI.newline()
    CUI.force_stop_progress(succesful=succesful)




def __generate_sheetmusic_musescore(midiPath: str,outputName: str) -> bool:
    """Uses musescore to generate a pdf, given a midi file path."""


    museScorePath = CONFIG["ENVIRONMENT"]["musescore4_path"]
    exportType = CONFIG["OPTIONS"]["export_type"]

    if not CONFIG["ADVANCED_OPTIONS"]["output_cleanly"]:
        outputPath = f"output\\sheet music\\"
    else:
        path = Path(os.getcwd())
        outputPath = f"{path.parent.absolute()}\\"


    # If the user doesn't have musecore
    if not os.path.isfile(museScorePath):
        CUI.warning("""MuseScore4 was not found. If you do want to use it, 
                    please install it and confirm that ENVIRONMENT.musescore4_path in config.toml is correct""")
        
        if not CONFIG["ADVANCED_OPTIONS"]["output_cleanly"]:
            return False

        CUI.newline()
        
        CUI.important("""Do you want to save the MIDI file instead? (yes/no)""")
        if CUI.yesno():
            os.rename(midiPath,f"{outputPath}{outputName}.mid")
            return True
        return False
        


    command = f'"{museScorePath}" -o "{outputPath}{outputName}.{exportType}" "{midiPath}"'

    Utils.sys_call(command)






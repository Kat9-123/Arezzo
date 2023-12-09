import cui.CUI as CUI
import core.Utils as Utils
from core.Configurator import CONFIG
import core.MIDIManager as MIDIManager
import os


def generate_midi_file(notes,tempo,outputName) -> None:
    """Takes a list of note objects, and a tempo and creates a MIDI file."""

    if not CONFIG["DEBUG"]["generate_sheet_music"]:
        return
    

    CUI.progress("Generating sheet music")

    # write it to disk

    if not CONFIG["ADVANCED_OPTIONS"]["output_cleanly"]:
        midiPath = f"output\\midi\\{outputName}.mid"
    else:
        midiPath = f"temp\\{outputName}.mid"

    MIDIManager.write_midi(notes,tempo,midiPath)

    CUI.diagnostic("MIDI",midiPath)



    succesful = __generate_sheetmusic_musescore(midiPath,outputName)
    CUI.force_stop_progress(succesful=succesful)

def __generate_sheetmusic_musescore(midiPath: str,outputName: str, succesful=True) -> bool:
    """Uses musescore to generate a pdf, given a midi file path."""
    museScorePath = CONFIG["ENVIRONMENT"]["musescore4_path"]
    exportType = CONFIG["OPTIONS"]["export_type"]

    if not os.path.isfile(museScorePath):
        CUI.warning("""MuseScore4 was not found, if you do want to use it, 
                    please install it and confirm that musescore4_path in config.toml
                    Do you want to save the MIDI file instead? (yes/no)""")
        return False
        
    if not CONFIG["ADVANCED_OPTIONS"]["output_cleanly"]:
        outputPath = f"output\\sheet music\\"
    else:
        outputPath = f""
    

    command = f'"{museScorePath}" -o "{outputPath}{outputName}.{exportType}" "{midiPath}"'
  

    Utils.sys_call(command)






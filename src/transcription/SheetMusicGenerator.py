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




def __save_midi(midiPath,midiName,outDir):

    outPath = f"{outDir}{midiName}.mid"
    os.rename(midiPath,outPath)
    CUI.important("MIDI saved to: {outpath}")
    

def generate_sheet_music(notes,tempo,outputName,key,timeSig) -> None:
    """Takes a list of note objects, and a tempo and creates a MIDI file."""

    if not CONFIG["DEBUG"]["generate_sheet_music"]:
        return
    

    CUI.progress("Generating sheet music")

    __confirm_temp_exists()


    outType = CONFIG["ARGS"]["out_type"].lower()
    if outType[0] != '.':
        outType = '.' + outType
    
    if outType == ".midi":
        outType = ".mid"
    



    if CONFIG["ADVANCED_OPTIONS"]["output_cleanly"]:
        path = Path(os.getcwd())
        baseOutDir = f"{path.parent.absolute()}\\"
        
    else:
        baseOutDir = "output\\"
        



    midiPath = f"temp\\{outputName}.mid"

    MIDIManager.write_midi(notes,tempo,midiPath,key,timeSig)

    CUI.diagnostic("MIDI",midiPath)



    if outType != ".mid":
        succesful = __generate_sheetmusic_musescore(midiPath,outputName,baseOutDir,outType)
    else:
        if CONFIG["ADVANCED_OPTIONS"]["output_cleanly"]:
            __save_midi(midiPath,outputName,baseOutDir)
            
        else:
            __save_midi(midiPath,outputName,f"{baseOutDir}\\midi\\")
        
        succesful = True


    __clear_temp()


    CUI.newline()
    CUI.force_stop_progress(succesful=succesful)




def __generate_sheetmusic_musescore(midiPath: str,outputName: str,baseOutDir,outType) -> bool:
    """Uses musescore to generate a pdf, given a midi file path."""

    museScorePath = CONFIG["ENVIRONMENT"]["musescore4_path"]


    # If the user doesn't have musecore
    if not os.path.isfile(museScorePath):
        CUI.warning("""MuseScore4 was not found. If you do want to use it, 
                    please install it and confirm that ENVIRONMENT.musescore4_path in config.toml is correct""")
        
        CUI.newline()
        
        CUI.important("""Do you want to save the MIDI file instead? (yes/no)""")
        if CUI.yesno():
            if CONFIG["ADVANCED_OPTIONS"]["output_cleanly"]:
                __save_midi(midiPath,outputName,baseOutDir)
                
            else:
                __save_midi(midiPath,outputName,f"{baseOutDir}\\midi\\")
            return True
        return False
        

    if CONFIG["ADVANCED_OPTIONS"]["output_cleanly"]:
        outputDir = baseOutDir
    else:
        outputDir = f"{baseOutDir}\\sheet music\\"

    command = f'"{museScorePath}" -o "{outputDir}{outputName}{outType}" "{midiPath}"'

    Utils.sys_call(command)






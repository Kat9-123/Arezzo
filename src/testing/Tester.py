import numpy as np

import testing.Scoring as Scoring
import transcription.Transcriber as Transcriber
import cui.CUI as CUI
import time
from core.Configurator import CONFIG

TEST_RESULTS_FOLDER = "testing\\results\\"



def test():


    data = np.loadtxt(CONFIG["ARGS"]["test"], delimiter=",", dtype=str)

    results = []
    for x,row in enumerate(data):

        # The first line and lines starting with # are skipped
        if x == 0 or row[0][0] == '#':
            continue
        

        path = "audio\\" + row[0].strip()
        comparePath = "testing\\" + row[1].strip()
        origTempo = float(row[2].strip())
        
        origKeySig = row[3].strip()


        while origKeySig[-1] == ' ':
            origKeySig = origKeySig[:-1]
        
        origKeySig = origKeySig.replace("s","#")


        origTimeSig = row[4].strip()

        minScore = round(float(row[5].strip()))

        
        processedMusic = Transcriber.transcribe(path,saveSheetMusic=CONFIG["ADVANCED_OPTIONS"]["test_save_sheet_music"],tempoOverride=origTempo)

    
        score = Scoring.score(processedMusic,origTempo,origKeySig,origTimeSig,comparePath)

        results.append([path,score,minScore])
    
    CUI.newline()
    CUI.newline()

    CUI.important("FINAL SCORES")

    CUI.print_colour(f"{'FILE':<36} {'NOTES':<6} {'TEMPO':<6} {'KEY':<6} {'TIME':<6} {'TOTAL':<6} {'MIN. SCORE':<6}",CUI.WHITE,end="\n")

    data = "FILE,NOTES,TEMPO O,TEMPO G,TEMPO S,KEY O,KEY G, KEY S,TIME O,TIME G,TIME S,TOTAL,MIN. SCORE\n"

    for result in results:
        path = result[0]
        score = result[1]
        origScore = result[2]
        
        
        colour = CUI.GREEN
    
        if score.totalScore < origScore:
            colour = CUI.RED
        
        CUI.print_colour(f"{path:<36} {score.noteScore:<6} {score.tempoScore:<6} {score.keyScore:<6} {score.timeScore:<6} {score.totalScore:<6} {origScore:<6}",colour,end="\n")
        data += f"{path},{score.noteScore}%,{score.tempoOrig},{score.tempoGen},{score.tempoScore}%,{score.keyOrig},{score.keyGen},{score.keyScore}%,{score.timeOrig},{score.timeGen},{score.timeScore}%,{score.totalScore}%,{origScore}%\n"

    data = data[:-1]
    name = TEST_RESULTS_FOLDER + f"TEST_{int(time.time())}.csv"

    with open(name, "w") as f:
        f.write(data)





import numpy as np

import Scoring
import Main
import ui.UI as UI


TESTS_PATH = "tests.csv"





def test():
    UI.print_colour("TESTING", UI.GREEN,end="\n")

    data = np.loadtxt(TESTS_PATH, delimiter=",", dtype=str)

    results = []
    for x,row in enumerate(data):
        if x == 0 or row[0][0] == '#':
            continue
        
        path = "audio\\" + row[0].replace(' ','')
        comparePath = "testing\\" + row[1].replace(' ','')
        origTempo = float(row[2].replace(' ',''))
        minScore = float(row[3].replace(' ',''))

        
        notes,tempo = Main.run(path,testMode=True,tempoOverride=-1)

        score = Scoring.score(notes,comparePath,tempo,origTempo)
        results.append([path,score,minScore])
    
    UI.newline()
    UI.newline()

    UI.print_colour("FINAL SCORES",UI.WHITE,end="\n")

    UI.print_colour(f"{'FILE':<30} {'SCORE':<6} {'MIN. SCORE':<6}",UI.WHITE,end="\n")
    for result in results:
        path = result[0]
        score = result[1]
        origScore = result[2]
        
        
        colour = UI.GREEN
    
        if score < origScore:
            colour = UI.RED
        
        UI.print_colour(f"{path:<30} {score:<6} {origScore:<6}",colour,end="\n")




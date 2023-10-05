from math import sqrt
import csv
from Configurator import CONFIG


def __average(x):
    return sum(x)/len(x)

KEY_NAMES = [
    "C Major",
    

    "C# Major",
    "D Major",
    "Eb Major", # D# Major
    "E Major",
    "F Major",
    "F# Major", #?
    "G Major",
    "Ab Major",
    "A Major",
    "Bb Major",
    "B Major",

    "C Minor",
    "C# Minor",
    "D Minor",
    "Eb Minor", # D# Minor
    "E Minor",
    "F Minor",
    "F# Minor",
    "G Minor",
    "G# Minor", #? 
    "A Minor",
    "Bb Minor",
    "B Minor"


]

def __get_profile() -> None:
    """Load the profile specified in CONFIG.ADVANCED_OPTIONS.KEY_PROFILE"""
    global MAJOR_PROFILE_, MINOR_PROFILE_
    if MAJOR_PROFILE_ != None and MINOR_PROFILE_ != None:
        return
    


    with open(CONFIG["ADVANCED_OPTIONS"]["key_profile"], newline='') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:

            if row[0].upper() == "MAJOR":
                MAJOR_PROFILE_ = []
                for i in row[1:]:
                    MAJOR_PROFILE_.append(float(i))

            elif row[0].upper() == "MINOR":
                MINOR_PROFILE_ = []
                for i in row[1:]:
                    MINOR_PROFILE_.append(float(i))

    return



MAJOR_PROFILE_ = None

MINOR_PROFILE_ = None

# https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
def __pearson_correlation(x,y):
    n = len(x) # Should be 12


    xAvg = __average(x)
    yAvg = __average(y)

    numerator = 0

    xDenominator = 0
    yDenominator = 0
    for i in range(n):
        xMinusAvg = x[i] - xAvg
        yMinusAvg = y[i] - yAvg

        numerator += (xMinusAvg * yMinusAvg)

        xDenominator += xMinusAvg * xMinusAvg
        yDenominator += yMinusAvg * yMinusAvg

    
    denominator = sqrt(xDenominator * yDenominator)

    return numerator/denominator


def __offset_notes(notes):
    first = notes[0]
    for i in range(len(notes)):
        if i == len(notes) - 1:
            notes[i] = first
            continue

        notes[i] = notes[i+1]
    
    return notes

CHROMAS = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

PROFILE_ = None

def __load_profile():
    pass

def guess_key(noteObjs):
    __get_profile()
    
    chromaDurations = [0]*12

    for noteObj in noteObjs:
        chroma = noteObj.note[:-1]
        i = CHROMAS.index(chroma)

        chromaDurations[i] += noteObj.duration


    





    greatest = -1_000
    iGreatest = -1
    for i in range(12):
        major = __pearson_correlation(MAJOR_PROFILE_,chromaDurations)
        if major > greatest:
            iGreatest = i
            greatest = major

        minor = __pearson_correlation(MINOR_PROFILE_,chromaDurations)
        if minor > greatest:
            iGreatest = i + 12
            greatest = minor
        print(KEY_NAMES[i],major,minor)

        chromaDurations = __offset_notes(chromaDurations)
    print(greatest,KEY_NAMES[iGreatest])
    input()

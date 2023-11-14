from math import sqrt
import csv

from Configurator import CONFIG
import cui.CUI as CUI


KEY_NAMES = [
    "C major",
    "C# major",
    "D major",
    "Eb major", # D# Major
    "E major",
    "F major",
    "Gb major", # F# Major
    "G major",
    "Ab major",
    "A major",
    "Bb major",
    "B major",



    "C minor",
    "C# minor",
    "D minor",
    "Eb minor", # D# Minor
    "E minor",
    "F minor",
    "F# minor",
    "G minor",
    "G# minor",
    "A minor",
    "Bb minor",
    "B minor"


]


def relative_key_check(a: str,b: str) -> bool:

    indexA = KEY_NAMES.index(a)
    indexB = KEY_NAMES.index(b)

    major = min(indexA,indexB)
    minor = max(indexA,indexB)


    minor += 3
    minor %= 12

    return major == minor

CHROMAS = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]


def __average(x):
    return sum(x)/len(x)



def __get_profiles() -> None:
    """Load the profile specified by ADVANCED_OPTIONS.KEY_PROFILE"""
    majorProfile = []
    minorProfile = []
    


    with open(CONFIG["ADVANCED_OPTIONS"]["key_profile"], newline='') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:

            if row[0].upper() == "MAJOR":
                for i in row[1:]:
                    majorProfile.append(float(i))

            elif row[0].upper() == "MINOR":
                for i in row[1:]:
                    minorProfile.append(float(i))

    return majorProfile,minorProfile





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


def guess_key(noteObjs) -> str:
    majorProfile, minorProfile = __get_profiles()
    
    chromaDurations = [0]*12

    for noteObj in noteObjs:
        chroma = noteObj.note[:-1]
        i = CHROMAS.index(chroma)

        chromaDurations[i] += noteObj.duration


    





    greatest = -1_000
    iGreatest = -1
    for i in range(12):
        major = __pearson_correlation(majorProfile,chromaDurations)
        if major > greatest:
            iGreatest = i
            greatest = major

        minor = __pearson_correlation(minorProfile,chromaDurations)
        if minor > greatest:
            iGreatest = i + 12
            greatest = minor


        CUI.diagnostic(f"{KEY_NAMES[i   ]:>8}",f"{round(major,2):>5}",end=" ")
        CUI.diagnostic(f"{KEY_NAMES[i+12]:>8}",f"{round(minor,2):>5}")

        chromaDurations = __offset_notes(chromaDurations)
    key = KEY_NAMES[iGreatest]


    CUI.newline()
    CUI.diagnostic("Key",f"{key} ({round(greatest,2)})"," ")

    return key

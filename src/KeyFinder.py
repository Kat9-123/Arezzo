from math import sqrt
import csv

from Configurator import CONFIG
import cui.CUI as CUI


KEY_NAMES = [
    "C Major",
    "C# Major",
    "D Major",
    "Eb Major", # D# Major
    "E Major",
    "F Major",
    "Gb Major", # F# Major
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
    "G# Minor",
    "A Minor",
    "Bb Minor",
    "B Minor"


]

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


def guess_key(noteObjs):
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

    CUI.newline()
    CUI.diagnostic("Key",f"{KEY_NAMES[iGreatest]} ({round(greatest,2)})"," ")

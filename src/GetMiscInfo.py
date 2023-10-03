from math import sqrt

def guess_time_signature():
    #T/4
    #end-(start - (start % T)) >= T
    pass


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

MAJOR_PROFILE = [
    6.35,
    2.23,
    3.48,
    2.33,
    4.38,
    4.09,
    2.52,
    5.19,
    2.39,
    3.66,
    2.29,
    2.88,
]

MINOR_PROFILE = [
    6.33, 2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17

]

# https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
def __pearson_correlation(x,y):
    n = len(x) # Should be 12

    result = 0

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

def __load_profile():
    pass

def guess_key(noteObjs):

    chromaDurations = [0]*12

    for noteObj in noteObjs:
        chroma = noteObj.note[:-1]
        i = CHROMAS.index(chroma)

        chromaDurations[i] += noteObj.duration


    





    greatest = -1_000
    iGreatest = -1
    for i in range(12):
        major = __pearson_correlation(MAJOR_PROFILE,chromaDurations)
        if major > greatest:
            iGreatest = i
            greatest = major

        minor = __pearson_correlation(MINOR_PROFILE,chromaDurations)
        if minor > greatest:
            iGreatest = i + 12
            greatest = minor
        print(KEY_NAMES[i],major,minor)

        chromaDurations = __offset_notes(chromaDurations)
    print(greatest,KEY_NAMES[iGreatest])
    input()

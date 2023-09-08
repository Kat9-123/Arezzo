import Graphing
import AudioProcessor
from Note import Note, NoteProbabilities
import Main
import ui.UI as UI

import librosa
import numpy as np
import copy


#https://en.wikipedia.org/wiki/Chroma_feature
# {C, C♯, D, D♯, E , F, F♯, G, G♯, A, A♯, B} => chroma
# 1, 5, 2, 7 => octave
# C4, A5, Db2 => note


# Rows, Frames



CHROMA = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

LOWEST_OCTAVE_DB = 5

HARMONIC_OCTAVE_MAX_DIFFERENCE_DB = 2


MAX_NOTE_DURATION = 4

MAX_N_VOICES = 4




freqs = np.ndarray


def get_notes(processedAudioData):
    """Takes in spectrum, chroma, onsets and tempo and returns all of the voices with their respective notes."""
    global finishedNotes,freqs
    freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT
    UI.progress("Generating Notes")

    spectrumRowCache = __cache_note_to_spectrum_row()
    UI.diagnostic("Cached Spectrum Rows", str(spectrumRowCache))
    UI.diagnostic("Onsets", str(processedAudioData.onsets))


    frameCount = processedAudioData.spectrum.shape[1]


    #start = onsets[0]
   # for x in range(len(onsets)):
    #    onsets[x] -= start



    for currentFrame in range(frameCount):
        #__get_notes_at_frame(currentFrame,processedAudioData)
        __process_info_at_frame(currentFrame,processedAudioData)

    UI.stop_spinner()
    return finishedNotes






def __row_to_note(row):

    return librosa.hz_to_note(freqs[row],unicode=False)

def __note_to_row(note):
    
    hz = librosa.note_to_hz(note)
    smallestDist = 10000
    smallestRow = -1

    for x,freq in enumerate(freqs):
        dist = abs(freq - hz)
        
        if dist < smallestDist:
            smallestRow = x
            smallestDist = dist
    
    if smallestRow == -1:
        UI.warning("Row corresponding to note not found!")
        return 0

   # UI.diagnostic("NOTE_TO_ROW","{} => {}".format(note,smallestRow))
    return smallestRow




def __get_volume_of_note(note,frame,processedAudioData):
    row = __note_to_row(note)

    return processedAudioData.spectrum[row,frame]



def __relative_volume_of_note(note,frame,processedAudioData):
    average = np.mean(processedAudioData.spectrum[:,frame])
    volume = __get_volume_of_note(note,frame,processedAudioData)

    #return volume/average * -1

    return volume/processedAudioData.loudest
def __cache_note_to_spectrum_row():
    freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT
    cache = {}
    lowestNote = "A0"
    lowestNoteDetected = False
    for x in range(1,len(freqs)):

        freq = freqs[x]
        note = librosa.hz_to_note(freq,unicode=False)
        if note == lowestNote:
            lowestNoteDetected = True
        if not lowestNoteDetected:
            continue
       
        cache[note] = x

    return cache


def __get_octave(note,onset,processedAudioData):
    strongest = -1000
    strongestI = -1



    for i in range(1,9):
        row = __note_to_row(note + str(i))

        values = []


        values.append(processedAudioData.spectrum[row,onset])



        val = np.mean(values)
        if val > strongest:
            strongest = val
            strongestI = i

        #if val > LOWEST_OCTAVE_DB:
        #   return i

    if strongestI == -1:
        UI.warning("Octave not found!")
        return 0
    return strongestI
        #if val > strongest:
        #    strongest = val
        #   strongestI = i
        
    #return strongestI

def ___get_octave(note,onset,processedAudioData):
    #onsets = processedAudioData.onsets.tolist()
    index = np.where(processedAudioData.onsets == onset)[0][0]
    
    if index < len(processedAudioData.onsets) - 1:
        nextOnset = processedAudioData.onsets[index+1] - 3
    else:
        nextOnset = onset + 15

    spectrum = processedAudioData.spectrum



    largestJump = -5000
    largestJumpIndex = -1

    print(f"{note} ", end="")
    previousStrength = 5000
    for i in range(1,9):
        row = __note_to_row(note + str(i))

        values = []


        for x in range(onset,nextOnset):
        #for r in range(-3,4):
        #    #for c in range(-1,6):
            
            values.append(spectrum[row,x])

        val = np.mean(values)
        print(f"{val} ",end="")
        if val - previousStrength > 15:
            largestJumpIndex = i
            largestJump = val - previousStrength

        previousStrength = val


        #if val > strongest:
         #   strongest = val
         #   strongestI = i

        #if val > LOWEST_OCTAVE_DB:
        #   return i

    if largestJumpIndex == -1:
        UI.warning("Octave not found!")
        return 0
    print()
    return largestJumpIndex
        #if val > strongest:
        #    strongest = val
        #   strongestI = i
        
    #return strongestI






def __harmonic_octave_detection():
    pass

def __get_key_signature():
    pass






currentNotes = {}
finishedNotes = []






def __linearalise_db(db):
    return 10**(db/10)


def __chromatic_neighbour_check(note,otherNote):

    chroma = note.chroma
    strength = note.startStrength



    otherChroma = otherNote.chroma
    otherStrength = otherNote.startStrength
    
    ## Check if the chromas are neighbours
    chromaIndex = CHROMA.index(chroma)
    otherChromaIndex = CHROMA.index(otherChroma)
    

    ## Neighbour check
    if abs(chromaIndex - otherChromaIndex) % 10 != 1:
       return (NoteProbabilities.KEEP,NoteProbabilities.KEEP)
    print("Chromatic neighbour check")

    if chroma == "B" and otherChroma == "C" and otherNote.octave - note.octave > 1:
        return (NoteProbabilities.KEEP,NoteProbabilities.KEEP)
    
    elif chroma == "C" and otherChroma == "B" and otherNote.octave - note.octave < -1:
        return (NoteProbabilities.KEEP,NoteProbabilities.KEEP)
    elif note.octave != otherNote.octave:
        return (NoteProbabilities.KEEP,NoteProbabilities.KEEP)

    

   # ## Both are strong enough
   # if strength > 0.7 and otherStrength > 0.7:
        

    ## Current note is weaker
    if otherStrength - strength > 0.1:
        return (NoteProbabilities.LOW,NoteProbabilities.KEEP)

    ## Current note is stronger
    if strength - otherStrength > 0.1:
        return (NoteProbabilities.KEEP,NoteProbabilities.LOW)

        
    return (NoteProbabilities.KEEP,NoteProbabilities.KEEP)
        

        
        

def __fifth_check(note,otherNote):
    chroma = note.chroma
    strength = note.startStrength



    otherChroma = otherNote.chroma
    otherStrength = otherNote.startStrength


    chromaIndex = CHROMA.index(chroma)
    otherChromaIndex = CHROMA.index(otherChroma)

    ## Upwards (5th)
    if (otherChromaIndex - chromaIndex) != 7:
        ## Downwards (4th)
        if (chromaIndex - otherChromaIndex) != 5:
            return(NoteProbabilities.KEEP,NoteProbabilities.KEEP)


    if strength - otherStrength > 0.3:

        return(NoteProbabilities.KEEP,NoteProbabilities.LOW)


    return (NoteProbabilities.KEEP,NoteProbabilities.KEEP)

    
def __bleed_over_check(note,frame,processedAudioData,previousFrame):
    global previousNotes

    if previousFrame == -1:
        return NoteProbabilities.KEEP

    if note.chroma not in previousNotes:
        return NoteProbabilities.KEEP
    
    deltaFrame = frame - previousFrame
    strength = 1 - 0.02 * deltaFrame

    print("BLEEDOVER STRENGTH", strength)
    if note.startStrength < strength:

        return NoteProbabilities.LOW
    
    return NoteProbabilities.KEEP

            


def __detect_invalid_notes(notes,frame,processedAudioData,previousFrame):
    

    for noteIndex,note in enumerate(notes):

        chroma = note.chroma

        #if note.startStrength > 0.5:
        #    note.set_probability_is_note(NoteProbabilities.HIGH)

        for otherIndex,otherNote in enumerate(notes):

            ## If note checking against itself
            otherChroma = otherNote.chroma
            if otherChroma == chroma:
                continue
            noteProbability = __bleed_over_check(note,frame,processedAudioData,previousFrame)
            notes[noteIndex].set_probability_is_note(noteProbability)

            noteProbability, otherProbability = __chromatic_neighbour_check(note,otherNote)
            notes[noteIndex].set_probability_is_note(noteProbability)
            notes[otherIndex].set_probability_is_note(otherProbability)
            noteProbability, otherProbability = __fifth_check(note,otherNote)

            notes[noteIndex].set_probability_is_note(noteProbability)
            notes[otherIndex].set_probability_is_note(otherProbability)

    for i in notes:
        print(i.probabilityIsNote)
    
    return notes





    

previousNotes = []
previousFrame = -1


def __add_new_notes():
    pass


def __remove_old_notes():
    pass

def __process_info_at_frame(frame,processedAudioData):
    global currentNotes,finishedNotes,previousNotes,previousFrame
    spectrum = processedAudioData.spectrum
    chroma = processedAudioData.chroma
    onsets = processedAudioData.onsets

   

    ## Find new notes
    if frame in processedAudioData.onsets:
        notes = __get_notes_at_frame(frame,processedAudioData)

        notes = __detect_invalid_notes(notes,frame,processedAudioData,previousFrame)
        previousFrame = frame
        previousNotes = []

        notesToRemove = []


        isFinalNote = (frame == processedAudioData.onsets[-1])


        playingNotesStrings = []
        for i in notes:
            playingNotesStrings.append(i.note)


        for note in currentNotes.keys():
            currentStrength = __note_to_row(note)
            #if currentStrength / currentNotes[note].startStrength < 0.96:
            
            idx = -1 if note not in playingNotesStrings else playingNotesStrings.index(note)

            if (idx == -1 or notes[idx].probabilityIsNote == NoteProbabilities.LOW or currentNotes[note].probabilityIsNote == NoteProbabilities.HIGH) and currentNotes[note].startFrame != frame:
                notesToRemove.append(note)
                if frame - currentNotes[note].startFrame < 4:
                    continue
                if currentNotes[note].set_duration(frame):
                    finishedNotes.append(currentNotes[note])





        for note in notesToRemove:
            currentNotes.pop(note)





        for note in notes:
            if note not in currentNotes:
               # startStrength = __linearalise_db(spectrum[__note_to_row(note),frame])
                note.start_note(processedAudioData)

                if note.note in currentNotes:
                   # if currentNotes[note.note].probabilityIsNote == NoteProbabilities.HIGH:
                    #    note.probabilityIsNote = NoteProbabilities.NORMAL
                    UI.warning(f"Note override: {note.note}")
                
                currentNotes[note.note] = note
                previousNotes.append(note.chroma)

        
    


        
        for note in currentNotes.keys():
            currentNotes[note].lifeTimeStrengths = np.append(currentNotes[note].lifeTimeStrengths, __relative_volume_of_note(note,frame,processedAudioData))
            if isFinalNote:
                if (currentNotes[note].set_duration(-1,isFinal=True)):
                    finishedNotes.append(currentNotes[note])


            
        


def __get_notes_at_frame(frame,processedAudioData):
    chroma = processedAudioData.chroma

    strongestNotes = []
    strengths = []

    for x,row in enumerate(chroma[:,frame]):
        chroma = CHROMA[x]
        octave = __get_octave(chroma,frame,processedAudioData)
        strength = __relative_volume_of_note(chroma + str(octave),frame,processedAudioData)
        if row < 0.25:
            continue
        

        #print(row)
        newNote = Note(chroma,octave,frame,__relative_volume_of_note(chroma + str(octave),frame,processedAudioData))
        # print()
        strongestNotes.append(newNote)


        
    if frame in processedAudioData.onsets:
        print(strongestNotes)
    return strongestNotes
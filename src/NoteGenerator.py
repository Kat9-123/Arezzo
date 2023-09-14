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
    global freqs
    freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT
   # freqs = librosa.fft_frequencies(sr=AudioProcessor.samplingRate,n_fft=AudioProcessor.N_FFT)
    UI.progress("Generating Notes")

    spectrumRowCache = __cache_note_to_spectrum_row()
    UI.diagnostic("Cached Spectrum Rows", str(spectrumRowCache))
    UI.diagnostic("Onsets", str(processedAudioData.onsets))


    frameCount = processedAudioData.spectrum.shape[1]

    #start = onsets[0]
   # for x in range(len(onsets)):
    #    onsets[x] -= start


    notes = []
    for currentFrame in range(frameCount):
        #__get_notes_at_frame(currentFrame,processedAudioData)
        notes = __process_info_at_frame(notes,currentFrame,processedAudioData)

    UI.stop_spinner()
    return notes






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


def ___get_octave(note,onset,processedAudioData):
    strongest = -1000
    strongestI = -1


    print(f"{note} ", end="")
    for i in range(1,9):
        row = __note_to_row(note + str(i))
        
        values = []


        values.append(processedAudioData.spectrum[row,onset])



        val = np.mean(values)
        if val > strongest:
            strongest = val
            strongestI = i
        print(f"{val} ",end="")

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

def __get_strength_of_octave(chroma,octave,onset,nextOnset,spectrum):
    row = __note_to_row(chroma + str(octave))


    #strength = __relative_volume_of_note(chroma + str(octave),onset,processedAudioData)
    values = []


    for c in range(onset,nextOnset):
        #for r in range(-2,2):
        #for c in range(-1,6):
        
                values.append(spectrum[row,c])

    return np.mean(values)

def __get_octave(note,onset,processedAudioData):
    #onsets = processedAudioData.onsets.tolist()
    index = np.where(processedAudioData.onsets == onset)[0][0]
    
    if index < len(processedAudioData.onsets) - 1:
        nextOnset = processedAudioData.onsets[index+1] - 3
    else:
        nextOnset = onset + 15

    spectrum = processedAudioData.spectrum




    print(f"{note} ", end="")

    index = -1
    previousStrength = 5000
    nextOctaveIsWeak = False
    for i in range(1,9):

        val = __get_strength_of_octave(note,i,onset,nextOnset,spectrum)
        #if note == "C#":

        print(f"{round(float(val),3)} ",end="")
        #if note == "B":
         #   print(val,previousStrength)

        if index != -1:
            continue

       
        if val > 4 and val - previousStrength > 15:
            if __get_strength_of_octave(note,i+1,onset,nextOnset,spectrum) < -5:
                nextOctaveIsWeak = True
        #if val - previousStrength > 40:
           # print()
            index = i


        previousStrength = val

        #if val > strongest:
         #   strongest = val
          #  strongestI = i

        #if val > LOWEST_OCTAVE_DB:
        #   return i

    #if strongestI == -1:
    #    UI.warning("Octave not found!")
    #    return 0
    print()
    return (index,nextOctaveIsWeak)
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
    

    

    midi = librosa.note_to_midi(note.note)
    otherMIDI = librosa.note_to_midi(otherNote.note)

    if abs(midi - otherMIDI) != 1:
        return (NoteProbabilities.KEEP,NoteProbabilities.KEEP)

    ## Current note is weaker
    if otherStrength - strength > 0.1:
        return (NoteProbabilities.LOW,NoteProbabilities.KEEP)

    ## Current note is stronger
    if strength - otherStrength > 0.1:
        return (NoteProbabilities.KEEP,NoteProbabilities.LOW)

        
    return (NoteProbabilities.KEEP,NoteProbabilities.KEEP)
        

        
#####################START STRENGTH ?

def __fifth_check(note,otherNote):
    chroma = note.chroma
    strength = note.startStrength



    otherChroma = otherNote.chroma
    otherStrength = otherNote.startStrength


    chromaIndex = CHROMA.index(chroma)
    otherChromaIndex = CHROMA.index(otherChroma)


    if librosa.note_to_midi(note.note) > librosa.note_to_midi(otherNote.note):
        return (NoteProbabilities.KEEP,NoteProbabilities.KEEP)

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

    prevNote = None
    for n in previousNotes:
        if n.note == note.note:
            prevNote = n
            break

    if prevNote == None:
        return NoteProbabilities.KEEP

    
    prevStrength = prevNote.get_average_strength()
    strength = note.startStrength

    if note.chroma == "F#":
        print(prevStrength, strength)

    if prevStrength - 0.05 > strength:
        return NoteProbabilities.LOW
    
    return NoteProbabilities.KEEP


    
    deltaFrame = frame - previousFrame
    strength = 0.015 * deltaFrame


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


playingNotes = []
def __process_info_at_frame(finishedNotes,frame,processedAudioData):
    global playingNotes,previousNotes,previousFrame



    for note in playingNotes:
        note.lifeTimeStrengths = np.append(note.lifeTimeStrengths, __relative_volume_of_note(note.note,frame,processedAudioData))


    if frame not in processedAudioData.onsets:
        return finishedNotes
    

    newNotes = __get_notes_at_frame(frame,processedAudioData)
    newNotes = __detect_invalid_notes(newNotes,frame,processedAudioData,previousFrame)

    previousFrame = frame
    previousNotes = []
    notesToRemove = []


   


    for playingNote in playingNotes:


        newSameNote = None
        for newNote in newNotes:
       
            if newNote.note != playingNote.note:
                continue

            newSameNote = newNote
            break


        noteNotPlaying = (newSameNote == None)
        if noteNotPlaying != True:
            noteLowProbability = (newSameNote.probabilityIsNote == NoteProbabilities.LOW)
            isDistinctNote = (newSameNote.startStrength > playingNote.get_average_strength())
        else:
            noteLowProbability = False
            isDistinctNote = False


        if (noteNotPlaying or noteLowProbability or isDistinctNote) and playingNote.startFrame != frame:
            notesToRemove.append(playingNote)


            if frame - playingNote.startFrame < 4:
                continue

            if playingNote.set_duration(frame):
                finishedNotes.append(playingNote)

            if not isDistinctNote and not noteNotPlaying:
                newNotes.remove(newSameNote)




    for note in notesToRemove:
        playingNotes.remove(note)


    for note in newNotes:

        # startStrength = __linearalise_db(spectrum[__note_to_row(note),frame])
        note.start_note(processedAudioData)


        playingNotes.append(note)
        previousNotes.append(note)


    if frame != processedAudioData.onsets[-1]:
        return finishedNotes
    
    for note in playingNotes:
        if (note.set_duration(-1,isFinal=True)):
            finishedNotes.append(note)

    return finishedNotes


  



def ___get_notes_at_frame(onset,processedAudioData):

    notes = []
    for chroma in CHROMA:
    #onsets = processedAudioData.onsets.tolist()
        index = np.where(processedAudioData.onsets == onset)[0][0]
        
        if index < len(processedAudioData.onsets) - 1:
            nextOnset = processedAudioData.onsets[index+1] - 3
        else:
            nextOnset = onset + 15

        spectrum = processedAudioData.spectrum



        strongest = -10000
        strongestI = -1

        print(f"{chroma} ", end="")

        test = -1
        previousStrength = 5000

        newNote = None
        for i in range(1,9):
            row = __note_to_row(chroma + str(i))


            strength = __relative_volume_of_note(chroma + str(i),onset,processedAudioData)
            values = []


            for c in range(onset,nextOnset):
                #for r in range(-2,2):
                #for c in range(-1,6):
                
                    values.append(spectrum[row,c])

            val = np.mean(values)
            #if note == "C#":

            print(f"{round(float(val),3)} ",end="")
            #if note == "B":
            #   print(val,previousStrength)

            if test != -1:
                continue
            if val > 0 and val - previousStrength > 15:
            #if val - previousStrength > 40:
            # print()
                newNote = Note(chroma,i,onset,__relative_volume_of_note(chroma + str(i),onset,processedAudioData))
                notes.append(newNote)
                test = i


            previousStrength = val

            #if val > strongest:
            #   strongest = val
            #  strongestI = i

            #if val > LOWEST_OCTAVE_DB:
            #   return i

        #if strongestI == -1:
        #    UI.warning("Octave not found!")
        #    return 0
        print()
    if onset in processedAudioData.onsets:
        UI.print_colour(strongestNotes, UI.GREEN)
    return notes
        


def __get_notes_at_frame(frame,processedAudioData):
    chromas = processedAudioData.chroma
    index = np.where(processedAudioData.onsets == frame)[0][0]
    
    if index < len(processedAudioData.onsets) - 1:
        nextOnset = processedAudioData.onsets[index+1] - 3
    else:
        nextOnset = frame + 15
    strongestNotes = []
    strengths = []

    for x,row in enumerate(chromas[:,frame]):
        chroma = CHROMA[x]
        octave,nextOctaveIsWeak = __get_octave(chroma,frame,processedAudioData)
        strength = __relative_volume_of_note(chroma + str(octave),frame,processedAudioData)

        #avgStrength = np.mean(chroma[x,frame:nextOnset-2])
        #or (octave != -1 and not nextOctaveIsWeak)
        if row > 0.25 : 
       # if row < 0.25:
        

        #print(row)
            newNote = Note(chroma,octave,frame,__relative_volume_of_note(chroma + str(octave),frame,processedAudioData))
            if nextOctaveIsWeak:
                newNote.set_probability_is_note(NoteProbabilities.LOW)
        # print()
            strongestNotes.append(newNote)


        
    if frame in processedAudioData.onsets:
        UI.print_colour(strongestNotes, UI.GREEN)
    return strongestNotes
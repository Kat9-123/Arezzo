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

TEMPO_BOUNDRY = 140

CHROMA = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

LOWEST_OCTAVE_DB = 5

HARMONIC_OCTAVE_MAX_DIFFERENCE_DB = 2


MAX_NOTE_DURATION = 4

MAX_N_VOICES = 4


IS_POLYPHONIC = True

def get_notes(processedAudioData):
    """Takes in spectrum, chroma, onsets and tempo and returns all of the voices with their respective notes."""
    global finishedNotes
    UI.progress("Generating Notes")
    
    spectrumRowCache = __cache_note_to_spectrum_row()
    UI.diagnostic("Cached Spectrum Rows", str(spectrumRowCache))
    UI.diagnostic("Onsets", str(processedAudioData.onsets))
    tempo = __fix_tempo(processedAudioData.tempo)

    frameCount = processedAudioData.spectrum.shape[1]



    #start = onsets[0]
   # for x in range(len(onsets)):
    #    onsets[x] -= start


    if IS_POLYPHONIC:
        for currentFrame in range(frameCount):
            #__get_notes_at_frame(currentFrame,processedAudioData)
            __process_info_at_frame(currentFrame,processedAudioData)

        UI.stop_spinner()
        return (finishedNotes,tempo)


    # IF HOMOPHONIC. Legacy
    notes = []
    for x,onset in enumerate(processedAudioData.onsets):



        strongestChroma = np.argsort(processedAudioData.chroma[:,onset])[::-1][:1]

        

        octave = __get_octave(CHROMA[strongestChroma[0]],onset,processedAudioData.spectrum)

        note = Note.Note(CHROMA[strongestChroma[0]],octave,onset,tempo,frameCount)
    
        if x == len(processedAudioData.onsets) -1:
            endSample = processedAudioData.onsets[-1] + 2
        else:
            endSample = processedAudioData.onsets[x+1]
        note.set_duration(endSample)

        notes.append(note)
    
    UI.stop_spinner()
    return (notes,tempo)


def __fix_tempo(rawTempo):
    """Correctly reduces tempo, based on TEMPO_BOUNDRY."""
    tempo = rawTempo

    while tempo > TEMPO_BOUNDRY:
        tempo //= 2
    
    UI.diagnostic("Corrected Tempo",tempo, "bpm")
    return tempo





def __row_to_note(row):
    freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT

    return librosa.hz_to_note(freqs[row],unicode=False)

def __note_to_row(note):
    freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT
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



def __get_octave(note,onset,spectrum):
    strongest = -1000
    strongestI = -1
    for i in range(1,9):
        val = np.mean([spectrum[__note_to_row(note + str(i)),onset],
                       spectrum[__note_to_row(note + str(i)),onset]+1,
                       spectrum[__note_to_row(note + str(i)),onset]+2])

        if val > strongest:
            strongest = val
            strongestI = i

       # if val > LOWEST_OCTAVE_DB:
        #    return i

    if strongestI == -1:
        UI.warning("Octave not found!")
        return 0
    return strongestI
        #if val > strongest:
        #    strongest = val
        #   strongestI = i
        
    #return strongestI






def __harmonic_octave_detection():
    pass

def __get_key_signature():
    pass

def __get_time_signature():
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
       return (note,otherNote)
    

    

   # ## Both are strong enough
   # if strength > 0.7 and otherStrength > 0.7:
        

    ## Current note is weaker
    if strength < 0.3 and otherStrength > 0.7:
        note.set_probability_is_note(NoteProbabilities.LOW)
        return (note,otherNote)

    ## Current note is stronger
    if otherStrength < 0.3 and strength > 0.7:
        
        otherNote.set_probability_is_note(NoteProbabilities.LOW)
        return (note,otherNote)
        
    return (note,otherNote)
        

        
        

def __fifth_check(note,otherNote):
    chroma = note.chroma
    strength = note.startStrength

    otherChroma = otherNote.chroma
    otherStrength = otherNote.startStrength


    chromaIndex = CHROMA.index(chroma)
    otherChromaIndex = CHROMA.index(otherChroma)

    ## Upwards (5th)
    if (otherChromaIndex - chromaIndex) != 7:
        return (note,otherNote)

    ## Downwards (4th)
    if (chromaIndex - otherChromaIndex) != 5:
        return (note,otherNote)
    
    if otherStrength < 0.3:
        otherNote.probabilityIsNote.set_probability_is_note(NoteProbabilities.LOW)
        return (note,otherNote)



    
def __bleed_over_check(note,frame,processedAudioData):
    pass

def __detect_invalid_notes(notes,frame=0,processedAudioData=0):
    

    for noteIndex,note in enumerate(notes):

        chroma = note.chroma

        for otherIndex,otherNote in enumerate(notes):

            ## If note checking against itself
            otherChroma = otherNote.chroma
            if otherChroma == chroma:
                continue
            newNote,newOther = __chromatic_neighbour_check(note,otherNote)
            notes[noteIndex] = newNote
            notes[otherIndex] = newOther
            newNote,newOther = __fifth_check(note,otherNote)

            notes[noteIndex] = newNote
            notes[otherIndex] = newOther

    return notes



        
    


def __process_info_at_frame(frame,processedAudioData):
    global currentNotes,finishedNotes
    spectrum = processedAudioData.spectrum
    chroma = processedAudioData.chroma
    onsets = processedAudioData.onsets
    #for x,row in enumerate(spectrum[:,sample]):
    notes = __get_notes_at_frame(frame,processedAudioData)
    notes = __detect_invalid_notes(notes)


    ## Find new notes
    if frame in processedAudioData.onsets:
       

        for note in notes:
            if note not in currentNotes:
               # startStrength = __linearalise_db(spectrum[__note_to_row(note),frame])
                note.start_note(processedAudioData)
                currentNotes[note.note] = note

        
    
        notesToRemove = []

        for note in currentNotes.keys():
           # currentStrength = __linearalise_db(spectrum[__note_to_row(note),frame])
            #if currentStrength / currentNotes[note].startStrength < 0.96:

            if note not in notes and currentNotes[note].startFrame != frame:
                notesToRemove.append(note)
                if frame - currentNotes[note].startFrame < 4:
                    continue
                if currentNotes[note].set_duration(frame):
                    finishedNotes.append(currentNotes[note])


        for note in notesToRemove:
            currentNotes.pop(note)

        
        for note in currentNotes.keys():
            chromaIndex = CHROMA.index(note[:-1])
            currentNotes[note].lifeTimeStrengths = np.append(currentNotes[note].lifeTimeStrengths, processedAudioData.chroma[chromaIndex,frame])



def __get_notes_at_frame(frame,processedAudioData):
    chroma = processedAudioData.chroma

    strongestNotes = []
    strengths = []

    for x,row in enumerate(chroma[:,frame]):
        if row < 0.25:
            continue
        
        chroma = CHROMA[x]
        octave = __get_octave(chroma,frame,processedAudioData.spectrum)
        newNote = Note(chroma,octave,frame,row)
        strongestNotes.append(newNote)


        
    #if frame in processedAudioData.onsets:
   #     print(strongestNotes)
    return strongestNotes
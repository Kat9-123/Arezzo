
import core.AudioProcessor as AudioProcessor
from transcription.NoteObj import NoteObj

import cui.CUI as CUI

import librosa
import numpy as np

import network.Manager as netManager
from core.Constants import *


#https://en.wikipedia.org/wiki/Chroma_feature
# {C, C♯, D, D♯, E , F, F♯, G, G♯, A, A♯, B} => chroma
# 1, 5, 2, 7 => octave
# C4, A5, Db2 => note
# NoteObj


# Rows, Frames



CHROMA = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]


cachedNoteRows = {}

def get_notes(processedAudioData):
    """Takes in spectrum, chroma, onsets and tempo and returns all of the voices with their respective notes."""
    global cachedNoteRows


    cachedNoteRows = __get_note_to_row_cache()

    CUI.debug(cachedNoteRows)
    CUI.newline()
    CUI.progress("Generating Notes")
    #print(__note_to_row("C9"))

    CUI.diagnostic("Onsets", str(processedAudioData.onsets))


    frameCount = processedAudioData.spectrum.shape[1]



    notes = []
    currentNotes = []
    for frame in range(processedAudioData.onsets[0],processedAudioData.onsets[-1]+1):
        notes = __process_frame(currentNotes,notes,frame,processedAudioData)


    CUI.force_stop_progress()
    return notes





def __get_note_to_row_cache():
    def __note_to_row(note,freqs):
        
        hz = librosa.note_to_hz(note)
        smallestDist = 10000
        smallestRow = -1

        for x,freq in enumerate(freqs):
            dist = abs(freq - hz)
            
            if dist < smallestDist:
                smallestRow = x
                smallestDist = dist
        
        if smallestRow == -1:
            CUI.warning("Row corresponding to note not found!")
            return 0

    # UI.diagnostic("NOTE_TO_ROW","{} => {}".format(note,smallestRow))
        return smallestRow
    
    #librosa.fft_frequencies(sr=AudioProcessor.samplingRate,n_fft=AudioProcessor.N_FFT)
    freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT
    
    cachedNoteRows = {}

    for octave in range(0,8):
        for chroma in CHROMA:
            note = chroma + str(octave)
            cachedNoteRows[note] = __note_to_row(note,freqs)

    cachedNoteRows[note] = __note_to_row("C8",freqs)

    return cachedNoteRows



def __delete_queued_notes(notes: list,queue: list):
    for qNote in queue:
        notes.remove(qNote)

    queue = []
    return notes


def __get_volume(note,frame,processedAudioData):

    return processedAudioData.spectrum[cachedNoteRows[note],frame]



def __process_frame(currentNotes: list,finishedNotes: list,frame: int,processedAudioData):
    
    if frame in processedAudioData.onsets:
        return __get_notes_at_frame(currentNotes,finishedNotes,frame,processedAudioData)

    for noteObj in currentNotes:
        strength = __get_volume(noteObj.note,frame-AudioProcessor.ONSET_TEMPORAL_LAG,processedAudioData)
        noteObj.add_strength(strength)

    return finishedNotes



def __get_notes_at_frame(currentNotes: list,finishedNotes: list,frame: int,processedAudioData) -> list:
    CUI.diagnostic("Frame",frame)

    # Notes playing at the current frame
    playingNotes = __model_get_notes(processedAudioData,frame)


    noteDeletionQueue = []

    # Loop through the notes that were already playing
    for curNoteObj in currentNotes:

        # If the note that was already playing is till playing, check if
        # it is the same note held, or the same note repeated
        if curNoteObj.note in playingNotes:
            
            newStrength = __get_volume(curNoteObj.note,frame-AudioProcessor.ONSET_TEMPORAL_LAG,processedAudioData)
            
            avgStrength = curNoteObj.get_average_strength()
            strengthDiff = (newStrength - avgStrength)
            CUI.debug((curNoteObj.note,newStrength,avgStrength, strengthDiff),debugControl=False)

            # The note was probably held
            if strengthDiff < -1:
                playingNotes.remove(curNoteObj.note)
                CUI.print_colour(f"-- {curNoteObj.note} ({strengthDiff:.2f})",CUI.YELLOW,end="\n")
                continue

        
        # curNote is no longer playing and should be finished
        curNoteObj.finish_note(frame)
        CUI.print_colour(f"<- {curNoteObj}",CUI.YELLOW,end="\n")
       # print(curNoteObj, curNoteObj.get_average_strength())
        finishedNotes.append(curNoteObj)
        noteDeletionQueue.append(curNoteObj)
            

    CUI.newline()
    currentNotes = __delete_queued_notes(currentNotes,noteDeletionQueue)


    for newNote in playingNotes:
        currentNotes.append(NoteObj(newNote,frame,processedAudioData))


    # Return if not final onset
    if frame != processedAudioData.onsets[-1]:
        return finishedNotes
    

    for note in currentNotes:
        note.finish_note(frame,isFinal=True)
        finishedNotes.append(note)

    return finishedNotes
    
        

    





def __model_get_notes(processedAudioData,frame):
    data = processedAudioData.spectrum[0:SPECTRUM_SIZE,frame]
    modelOutput = netManager.get_model_output(data)


    notes = []
    #print(modelOutput.tolist())
    for x,i in enumerate((modelOutput.tolist())):
        if i == 0:
            continue
        octave, chroma = divmod(x + 9,12)
        chroma = CHROMA[chroma]
        note = chroma + str(octave)
        CUI.print_colour(f"-> {note}",CUI.YELLOW,end="\n")
        notes.append(note)


    return notes





  
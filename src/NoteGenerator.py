import Graphing
import AudioProcessor
from Note import Note, NoteProbabilities
import Main
import cui.CUI as CUI

import librosa
import numpy as np
import copy
import network.Manager as netManager


#https://en.wikipedia.org/wiki/Chroma_feature
# {C, C♯, D, D♯, E , F, F♯, G, G♯, A, A♯, B} => chroma
# 1, 5, 2, 7 => octave
# C4, A5, Db2 => note


# Rows, Frames


SHOW_OCTAVE_INFO = False



CHROMA = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

LOWEST_OCTAVE_DB = 5

HARMONIC_OCTAVE_MAX_DIFFERENCE_DB = 2


MAX_NOTE_DURATION = 4






freqs = np.ndarray


def get_notes(processedAudioData):
    """Takes in spectrum, chroma, onsets and tempo and returns all of the voices with their respective notes."""
    global freqs
    #freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT
   # freqs = librosa.fft_frequencies(sr=AudioProcessor.samplingRate,n_fft=AudioProcessor.N_FFT)
    CUI.progress("Generating Notes")
    #print(__note_to_row("C9"))

    #spectrumRowCache = __cache_note_to_spectrum_row()
    #UI.diagnostic("Cached Spectrum Rows", str(spectrumRowCache))
    CUI.diagnostic("Onsets", str(processedAudioData.onsets))


    frameCount = processedAudioData.spectrum.shape[1]

    #start = onsets[0]
   # for x in range(len(onsets)):
    #    onsets[x] -= start


    notes = []
    for currentFrame in processedAudioData.onsets:
        #__get_notes_at_frame(currentFrame,processedAudioData)
        __model_get_notes(processedAudioData,currentFrame)

    CUI.stop_spinner()
    return notes












currentNotes = {}
finishedNotes = []










    

previousNotes = []
previousFrame = -1





def __model_get_notes(processedAudioData,frame):
    data = processedAudioData.spectrum[0:6222,frame]
    modelOutput = netManager.get_model_output(data)
    print(modelOutput.tolist())
    for x,i in enumerate((modelOutput.tolist())):
        if i == 0:
            continue
        octave, chroma = divmod(x + 9,12)
        chroma = CHROMA[chroma]
        CUI.print_colour(chroma + str(octave),CUI.RED,end="\n")
    return 

playingNotes = []
def __process_info_at_frame(finishedNotes,frame,processedAudioData):
    global playingNotes,previousNotes,previousFrame
   

            



    for note in playingNotes:
        note.lifeTimeStrengths = np.append(note.lifeTimeStrengths, __relative_volume_of_note(note.note,frame,processedAudioData))


    if frame not in processedAudioData.onsets:
        return finishedNotes

    modelOutput = __model_get_notes(processedAudioData,frame)
  

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


  
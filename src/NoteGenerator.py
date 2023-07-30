import Graphing
import AudioProcessor
import Note
import Main
import ui.UI as UI

import librosa
import numpy as np


#https://en.wikipedia.org/wiki/Chroma_feature
# {C, C♯, D, D♯, E , F, F♯, G, G♯, A, A♯, B} => chroma
# 1, 5, 2, 7 => octave
# C4, A5, Db2 => note


TEMPO_BOUNDRY = 140

CHROMA = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

LOWEST_OCTAVE_DB = 5

HARMONIC_OCTAVE_MAX_DIFFERENCE_DB = 2


MAX_NOTE_DURATION = 4

MAX_N_VOICES = 2


IS_POLYPHONIC = True

def get_notes_voices(spectrum, chroma, onsets, rawTempo):
    """Takes in spectrum, chroma, onsets and tempo and returns all of the voices with their respective notes."""
    global finishedNotes
    UI.progress("Generating Notes")
    
    spectrumRowCache = __cache_note_to_spectrum_row()
    UI.diagnostic("Cached Spectrum Rows", str(spectrumRowCache))
    UI.diagnostic("Onsets", str(onsets))
    tempo = __fix_tempo(rawTempo)


    octaves = __get_octaves(spectrum,onsets)


    #start = onsets[0]
   # for x in range(len(onsets)):
    #    onsets[x] -= start


    if IS_POLYPHONIC:
        for i in range(spectrum.shape[1]):
            __process_info_at_sample(spectrum,chroma,i,onsets,spectrumRowCache,tempo)

        UI.stop_spinner()
        return ([finishedNotes],tempo)


    # IF HOMOPHONIC
    notes = []
    for x,onset in enumerate(onsets):



        strongestChroma = np.argsort(chroma[:,onset])[::-1][:1]

        

        octave = __get_octave(CHROMA[strongestChroma[0]],onset,spectrum)

        note = Note.Note(CHROMA[strongestChroma[0]],octave,onset,tempo)
    
        if x == len(onsets) -1:
            endSample = onsets[-1] + 2
        else:
            endSample = onsets[x+1]
        note.set_duration(endSample)

        notes.append(note)
    
    UI.stop_spinner()
    return ([notes],tempo)


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
    hz=   librosa.note_to_hz(note)
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
        val = spectrum[__note_to_row(note + str(i)),onset]
        #if val > strongest:
        #    strongest = val
        #    strongestI = i

        if val > LOWEST_OCTAVE_DB:
            return i

    if strongestI == -1:
        UI.warning("Octave not found!")
        return 0
    return strongestI
        #if val > strongest:
        #    strongest = val
        #   strongestI = i
        
    #return strongestI


def __get_octaves(spectrum,onsets):
    """Deprecated"""
    spectrum = spectrum.argmax(axis=0)
    freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT
    print(freqs)
    octaves = np.zeros(shape=[10,AudioProcessor.pointCount])
    for x,i in enumerate(spectrum):
        if i == 0:
            continue
        octaves[int(librosa.hz_to_note(freqs[i])[-1:]),x] = 1
        #print()
    #Graphing.specshow(octaves,AudioProcessor.samplingRate,location=3,xType="s",yLabel="Octave")


    return octaves
    bins = spectrum.argmax(axis=0)
    print(bins)
    freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT
    

    arr = np.zeros(shape=[10,len(onsets)])
    for x,i in enumerate(bins):
        if i == 0:
            continue
        arr[int(librosa.hz_to_note(freqs[i])[-1:]),x] = 1
        #print()

    return arr
    #img = librosa.display.specshow(arr,ax=ax[3],x_axis="s")
   # 








def __harmonic_octave_detection():
    pass

def __get_key_signature():
    pass

def __get_time_signature():
    pass




currentNotes = {}
finishedNotes = []



def __guess_voice_count_at_sample(spectrum,sample):



    notes = {}
    for octave in range(1,7):
        for chroma in CHROMA:
            
            note = chroma + str(octave)
            row = spectrum[__note_to_row(note),sample]

            if row < 15:
                continue
            
            notes[note] = row


    #print(notes)

    # Check for chromatic neighbours
    keys = notes.keys()
    #print(keys)
    notesDeletionQueue = []
    skipNeighbour = False
    for note in keys:
        if skipNeighbour:
            skipNeighbour = False
            continue
        
        chroma = note[:-1]
        octave = int(note[-1:])
        for i in range(octave+1,7):
            octaveNote = chroma + str(i)
            if octaveNote in notes:
                notesDeletionQueue.append(octaveNote)

        # Check fifth
        

        noteIndex = CHROMA.index(chroma)
        
        # B4 => C5
        if noteIndex == 11:
            noteIndex = -1
            octave += 1
        
        chromaticNextNeighbour = CHROMA[noteIndex+1] + str(octave)

        #print(note,chromaticNextNeighbour)

        
        if not chromaticNextNeighbour in notes:
            continue
        row = notes[note]
        neighbourRow = notes[chromaticNextNeighbour]
    
        difference = row - neighbourRow

        # Neighbour is greater
        if difference < -2.5:
            notesDeletionQueue.append(note)

        # Row is greater
        if difference > 2.5:
            notesDeletionQueue.append(chromaticNextNeighbour)
                

    #print("Deleted", notesDeletionQueue)
    for note in notesDeletionQueue:
        notes.pop(note)


    nVoices = 0
    for note in notes:
        nVoices += 1

    #UI.diagnostic("Voice count",nVoices)
    return nVoices
    nVoices = 0
    strongest = np.array()
    for octave in range(1,7):
        for chroma in CHROMA:
            note = chroma + str(octave)
            row = spectrum[__note_to_row(note),sample]
            if row > 15:
                strongest.append(row)
                print("NOTE",note,row)
                nVoices += 1
    

    UI.diagnostic("Voice count",nVoices)
    return nVoices
    nVoices = 0
    strongestSpectrum = np.sort(spectrum[:,sample])
    for row in spectrum[:,sample]:
        if row > 25:
            nVoices += 1
    UI.diagnostic("Voice count",nVoices)
    return nVoices
    


def __process_info_at_sample(spectrum,chroma,sample,onsets,spectrumRowCache,tempo):
    global currentNotes,finishedNotes
    #for x,row in enumerate(spectrum[:,sample]):
    if sample in onsets:

        voices = __guess_voice_count_at_sample(spectrum,sample)
        strongestChromas = np.argsort(chroma[:,sample])[::-1][:MAX_N_VOICES]
        found = 0
        for x in strongestChromas:
            if found >= voices:
                continue
            
            
            row = chroma[x,sample]
            if row < 0:
                continue
            
            found += 1
                
            octave = __get_octave(CHROMA[x],sample,spectrum)

            note = CHROMA[x] + str(octave)


            if note not in currentNotes:
                currentNotes[note] = Note.Note(CHROMA[x],octave,sample,tempo)

        
    
        notesToRemove = []

        for note in currentNotes.keys():
            # spectrum[__note_to_row(note),sample] <= 23 and 
            if currentNotes[note].startSample != sample:
                currentNotes[note].set_duration(sample)
                notesToRemove.append(note)

        for note in notesToRemove:
            finishedNotes.append(currentNotes[note])
            currentNotes.pop(note)

    return
    freqs = np.arange(1, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT

    sampleExpectedNotes = {}

    for x,row in enumerate(spectrum[:,sample]):
        if row <= 0:
            continue
            
        if sample in onsets:
            UI.set_colour(UI.BLUE)
        note = librosa.hz_to_note(freqs[x],unicode=False)
        print(sample, note, row)

        if note in sampleExpectedNotes:
            if row > sampleExpectedNotes[note]:
                sampleExpectedNotes[note] = row
        else:
            sampleExpectedNotes[note] = row

        UI.set_colour(UI.WHITE)
    UI.set_colour(UI.YELLOW)
    print(sampleExpectedNotes)
    UI.set_colour(UI.WHITE)
    
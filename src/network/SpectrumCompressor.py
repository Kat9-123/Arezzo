# Very simple but quite effective compression of the training data (notes + spectrum)




import random
import math
import numpy as np


SPECTRA_PATH = "learning\\spectra\\"

PRECISION = 10**3
NOTE_COUNT_LOCATION = 0
SPECTRUM_SIZE_LOCATION = 1
SAMPLE_COUNT_LOCATION = 2

def __compress_notes(notes,noteCount,sampleCount):
    noteWordCount = math.ceil(noteCount/16)



    noteWords = np.zeros(noteWordCount*sampleCount,dtype=np.uint16)


    
    for i,sample in enumerate(notes):
        
        currentWord = noteWordCount * i
        currentBit = 0
        for note in sample:

            val = note & 1

            noteWords[currentWord] |= (val << (15-currentBit))

            currentBit += 1

            # If the currentWord is full, move on to the next
            if currentBit == 16:
                currentBit = 0
                currentWord += 1

    
    return noteWords.astype(np.uint16)

def __compress_spectrum(spectrum):
    spectrum = spectrum.ravel()

    # Move negative into positive
    spectrum += 64

    # Discard unnecessary precision
    spectrum *= (PRECISION/2)


    return spectrum.astype(np.uint16)





def __generate_header(noteCount,spectrumSize,sampleCount):
    header = np.zeros(4)
    # Notecount -> 2 bytes
    header[NOTE_COUNT_LOCATION] = noteCount


    # Spectrumsize -> 2 bytes
    header[SPECTRUM_SIZE_LOCATION] = spectrumSize

    
    # Samplecount -> 4 bytes
    # Mask left part of number
    header[SAMPLE_COUNT_LOCATION] = (sampleCount & 0xFFFF0000) >> 15

    # Mask right part of number
    header[SAMPLE_COUNT_LOCATION+1] = (sampleCount & 0x0000FFFF)

    
    return header.astype(np.uint16)



def compress(notes,spectrum,fileName):
    
    noteCount = notes.shape[1]
    spectrumSize = spectrum.shape[1]
    sampleCount = notes.shape[0]

    header = __generate_header(noteCount,spectrumSize,sampleCount)
    

    


    
    
    compressedSpectrum = __compress_spectrum(spectrum)
    compressedNoteInts = __compress_notes(notes,noteCount,sampleCount)

    compressed = np.concatenate([header,compressedSpectrum, compressedNoteInts])
    

    

    compressed.tofile(f"{SPECTRA_PATH}{fileName}.csd")







def __retrieve_header(headerInts):
    noteCount = int(headerInts[NOTE_COUNT_LOCATION])
    spectrumSize = int(headerInts[SPECTRUM_SIZE_LOCATION])

    leftSampleCount = int(headerInts[SAMPLE_COUNT_LOCATION])

    rightSampleCount = int(headerInts[SAMPLE_COUNT_LOCATION+1])


    sampleCount = (leftSampleCount << 15) | rightSampleCount


    return (noteCount,spectrumSize,sampleCount)





def __decompress_spectrum(compressedSpectrum,spectrumSize):

    spectrum = compressedSpectrum.astype(float)

    spectrum /= (PRECISION / 2)
    spectrum -= 64

    spectrum = np.reshape(spectrum,(-1,spectrumSize))
    return spectrum


def __decompress_notes(compressedNotes,noteCount,sampleCount):
    notes = np.zeros((sampleCount,noteCount),dtype=float)
    noteWordCount = math.ceil(noteCount/16)


    
    for i,sample in enumerate(notes):
        
        currentWord = noteWordCount * i
        currentBit = 0
        for note in range(len(sample)):

            curWord = compressedNotes[currentWord]

            notes[i][note] = (curWord & (1 << (15 - currentBit))) >> (15-currentBit)

            currentBit += 1

            # If the currentInt16 is full, move on to the next
            if currentBit == 16:
                currentBit = 0
                currentWord += 1

    
    return notes


def decompress(fileName):
    
    compressed = np.fromfile(f"{SPECTRA_PATH}{fileName}",dtype=np.uint16)
    
    # First 64 bits are header (4 uint16s)
    header = compressed[0:4]

    noteCount,spectrumSize,sampleCount = __retrieve_header(header)


    spectrumEndIndex = 4 + spectrumSize*sampleCount

    compressedSpectrum = compressed[4:spectrumEndIndex]
    compressedNotes = compressed[spectrumEndIndex:]

    spectrum = __decompress_spectrum(compressedSpectrum,spectrumSize)
    notes = __decompress_notes(compressedNotes,noteCount,sampleCount)
    

    return (notes,spectrum)





def test():
    SPECTRUM_LOWER_BOUND = -50
    SPECTRUM_UPPER_BOUND = 50
    MAX_COMPRESSED_DIFFERENCE = 0.002
    SAMPLE_COUNT = 5000
    FILE_NAME = "TEST"


    SPECTRUM_SIZE = random.randint(1000,10000)
    NOTE_COUNT = random.randint(5,100)

    


    spectrum = (SPECTRUM_UPPER_BOUND - SPECTRUM_LOWER_BOUND) * np.random.rand(SAMPLE_COUNT,SPECTRUM_SIZE) + SPECTRUM_LOWER_BOUND


    fNotes = np.random.rand(SAMPLE_COUNT,NOTE_COUNT)

    fNotes[fNotes >= 0.5] = 1
    fNotes[fNotes < 0.5] = 0

    notes = fNotes.astype(np.uint8)

    print("Spectrum size:",SPECTRUM_SIZE)
    print("Note count:", NOTE_COUNT)


    compress(np.copy(notes),np.copy(spectrum),FILE_NAME)
    print("DONE COMPRESSING")


    rNotes,rSpectrum = decompress(FILE_NAME + ".csd")
    print("DONE DECOMPRESSING")
    
    for y in range(spectrum.shape[0]):
        for x in range(spectrum.shape[1]):
            assert abs(spectrum[y][x] - rSpectrum[y][x]) < MAX_COMPRESSED_DIFFERENCE

    for y in range(notes.shape[0]):
        for x in range(notes.shape[1]):
            assert notes[y][x] == rNotes[y][x]


    print("Passed tests!")


import os
import numpy as np
import math
import torch

from torch.utils.data import Dataset

import cui.CUI as CUI
import network.SpectrumCompressor as SpectrumCompressor
from core.Constants import *


SPECTRA_PATH = "learning\\spectra\\"


class SpectrumDataset(Dataset):

    size: int = 0
    path: str
    spectrumSize: int
    noteCount: int
    device = ""

    fileSizes: list = []
    fileStreams: list = []



    def __get_info(self,path):
        fileStream = open(path, "rb")

        header = fileStream.read(CSD_HEADER_SIZE)
        

    
        headerArray = np.frombuffer(header,dtype=np.uint16)

        return fileStream,SpectrumCompressor.retrieve_header(headerArray)

    def __init__(self, _path,_device):
        self.device = _device


        if os.path.isdir(f"{SPECTRA_PATH}{_path}"):
            self.path = f"{SPECTRA_PATH}{_path}"
            filePaths = sorted(os.listdir(self.path))
            
            
        else:
            path, file = os.path.split(_path)
            filePaths = [file]
            self.path = f"{SPECTRA_PATH}{path}"
            
            #self.noteCount, self.spectrumSize, self.size = self.__get_info(self.path)
            #self.singleFile = True
    
        for file in filePaths:
            fileStream,(noteCount,spectrumSize,fileSize) = self.__get_info(f"{self.path}\\{file}")
            if noteCount != NOTE_COUNT:
                raise Exception(f"Note count of {file} ({noteCount}) does not match expected value ({NOTE_COUNT})")
            if spectrumSize != SPECTRUM_SIZE:
                raise Exception(f"Spectrum size of {file} ({spectrumSize}) does not match expected value ({NOTE_COUNT})")

            self.fileSizes.append(fileSize)
            self.size += fileSize
            self.fileStreams.append(fileStream)
        CUI.debug(self.fileSizes)

    def __len__(self):
        return self.size

    def __getitem__(self, globalIndex):


        totalSize = 0
        fileIndex = 0
        idx = 0

        # Find the correct file to read
        for i,size in enumerate(self.fileSizes):
            
            if totalSize + size > globalIndex:
                fileIndex = i
                idx = globalIndex - totalSize
                break
            totalSize += size

        spectrumIndex = CSD_HEADER_SIZE # Skip the header
        spectrumIndex += idx*SPECTRUM_SIZE * 2 # Each spectrum element is 2 bytes




        notesIndex = CSD_HEADER_SIZE + SPECTRUM_SIZE*self.fileSizes[fileIndex]*2

        notesIndex += idx*(math.ceil(NOTE_COUNT/16)*2)

        fileStream = self.fileStreams[fileIndex]
        fileStream.seek(spectrumIndex)
        rawSpectrum = fileStream.read(SPECTRUM_SIZE*2)

        fileStream.seek(notesIndex)
        rawNotes = fileStream.read(math.ceil(NOTE_COUNT/16)*2)


        spectrumArray = np.frombuffer(rawSpectrum,dtype=np.uint16)
        noteArray = np.frombuffer(rawNotes,dtype=np.uint16)

        spectrum = SpectrumCompressor.decompress_line(spectrumArray)
        notes =  SpectrumCompressor.decompress_note_line(noteArray,NOTE_COUNT)

        spectrum = torch.tensor(spectrum, dtype=torch.float32)
        notes = torch.tensor(notes, dtype=torch.float32)

        return spectrum, notes
    

    def __del__(self):
        for fileStream in self.fileStreams:
            fileStream.close()
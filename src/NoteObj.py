import cui.CUI as CUI
from ProcessedAudioData import ProcessedAudioData
import AudioProcessor
import Utils


import numpy as np
import math
import librosa
from enum import Enum




# 2 -> Semiquavers
# 3 -> Demisemiquavers
# etc.










class NoteObj:
    start: float = 0
    duration: float = 0
    note: str

    
    __startFrame: int
    __processedAudioData: ProcessedAudioData
    __lifetimeStrengths: list = []


    def __init__(self,_note,_startFrame,_processedAudioData) -> None:
        self.note = _note

        self.__startFrame = _startFrame
        self.__processedAudioData = _processedAudioData


    def add_strength(self,strength):
        self.__lifetimeStrengths.append(strength)
        

    def get_average_strength(self):
        return np.mean(self.__lifetimeStrengths) # Median?


    def __repr__(self) -> str:
        if self.duration == 0:
            return f"(@{self.note} {self.__startFrame:.2f})"
    
        return f"({self.note} {self.start:.2f}:{self.duration:.2f})"



    def finish_note(self,endFrame,isFinal=False):


  

        tempo = self.__processedAudioData.tempo
        frameDuration = self.__processedAudioData.frameDuration
      
        offset = self.__processedAudioData.onsets[0]

        offsetStartFrame = self.__startFrame - offset
        offsetEndFrame = endFrame - offset

        self.start = Utils.snap_to_beat(offsetStartFrame * (tempo/60) * frameDuration)
        if not isFinal:
            self.duration = Utils.snap_to_beat((offsetEndFrame - offsetStartFrame)  * (tempo/60) * frameDuration)
        else:
            self.duration = 2
        
        CUI.print_colour(f"{self.note} {round(self.start,4)} {round(self.duration,4)}                                \n",CUI.CYAN)
    
        return True
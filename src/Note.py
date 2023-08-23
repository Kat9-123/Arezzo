import ui.UI as UI
from ProcessedAudioData import ProcessedAudioData
import AudioProcessor



import numpy as np
import math
import librosa
from enum import Enum


NOTE_DURATONS = [
    8, # Breve
    4, # Semibreve
    2, # Minim
    1, # Crotchet
    0.5, # Quaver
    0.25, # Semiquaver
  #  0.125 # Demisemiquaver

]



# 2 -> Semiquavers
# 3 -> Demisemiquavers
# etc.
NOTE_DEPTH = 2**2






class NoteProbabilities(Enum):
    LOW = 1
    KEEP = 0
    NORMAL = 2
    HIGH = 3


class Note:
    duration: float
    chroma: str
    octave: int

    note: str

    midi: int
    start: float

    lifeTimeStrengths = np.array([])

    startStrength: float


    probabilityIsNote = NoteProbabilities.NORMAL


    startFrame: int

    processedAudioData: ProcessedAudioData



    def __init__(self,_chroma,_octave,_startFrame,_startStrength) -> None:
        self.chroma = _chroma
        self.octave = _octave
        self.startFrame = _startFrame
        self.startStrength = _startStrength

        if self.startStrength > 0.8:
            self.probabilityIsNote = NoteProbabilities.HIGH

        self.note = self.chroma + str(self.octave)

    def __repr__(self) -> str:
        return f"Note: {self.chroma}{str(self.octave)}, {str(self.startStrength)}"

    def set_probability_is_note(self,_probability):
        if _probability == NoteProbabilities.KEEP:
            return
    
        self.probabilityIsNote = _probability
        #print(self.probabilityIsNote)

    def start_note(self,_processedAudioData):
        

        self.processedAudioData = _processedAudioData

    
        self.midi = librosa.note_to_midi(self.chroma + str(self.octave))



    def snap_time_to_beat(self,time):
        #print(time, "=>", round(time,5))
       # return round(time,5)




        if time == 0.0:
            UI.warning("Zero Time")
            return 0.0
        
        result =  time * NOTE_DEPTH

        result = round(result)

        result /= NOTE_DEPTH



        #print(time, "=>", result)
        return result






    def set_duration(self,endFrame,isFinal=False):


        minLifeTimeStrength = 0
        #minFrameLength

        match self.probabilityIsNote:
            case NoteProbabilities.LOW:
                minLifeTimeStrength = 0.75
            case NoteProbabilities.NORMAL:
                minLifeTimeStrength = 0.25
            case NoteProbabilities.HIGH:
                minLifeTimeStrength = 0
        
        #print(self.probabilityIsNote)

        if np.mean(self.lifeTimeStrengths) < minLifeTimeStrength:
           print("Note failed average check")
           return False
        
        #if self.endFrame - self.startFrame

        tempo = self.processedAudioData.tempo
        frameDuration = self.processedAudioData.frameDuration
      
        offset = self.processedAudioData.onsets[0]
        offsetStartFrame = self.startFrame - offset
        offsetEndFrame = endFrame - offset

        self.start = self.snap_time_to_beat(offsetStartFrame * (tempo/60) * frameDuration)
        if not isFinal:
            self.duration = self.snap_time_to_beat((offsetEndFrame - offsetStartFrame)  * (tempo/60) * frameDuration)
        else:
            self.duration = 2
        

        debugNote = self.chroma
        if len(self.chroma) == 1:
            debugNote += " "
        
        debugNote += str(self.octave)

        UI.print_colour("{} {} {}                                   \n".format(debugNote, round(self.start,4), round(self.duration,4)),UI.CYAN)
        return True
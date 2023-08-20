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



class NoteProbabilities(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2


class Note:
    duration: float
    chroma: str
    octave: int

    note: str

    midi: int
    start: float

    lifeTimeStrengths = np.array([])

    startStrength: float


    probabilityIsNote = NoteProbabilities.HIGH


    startFrame: int

    processedAudioData: ProcessedAudioData


    def __init__(self,_chroma,_octave,_startFrame,_startStrength) -> None:
        self.chroma = _chroma
        self.octave = _octave
        self.startFrame = _startFrame
        self.startStrength = _startStrength

        self.note = self.chroma + str(self.octave)

    def set_probability_is_note(self,_probability):
        self.probabilityIsNote = _probability
        match self.probabilityIsNote:
            case NoteProbabilities.LOW:
                print("LOW")
            case NoteProbabilities.NORMAL:
                print("NORMAL")
            case NoteProbabilities.HIGH:
                print("HIGH")

    def start_note(self,_processedAudioData,):
        

        self.processedAudioData = _processedAudioData
    
        self.midi = librosa.note_to_midi(self.chroma + str(self.octave))


    def snap_time_to_beat(self,time):
        #print(time, "=>", round(time,5))
       # return round(time,5)
        integerTime,decimalTime = divmod(time,1)
        #print(time,math.log2(1/decimalTime))
        result = 1.0/pow(2,round(math.log2(1/decimalTime))) + integerTime
       # print(time, "=>", result)
        return result

        initialTime = time
        for duration in NOTE_DURATONS:
            #1.2
            while time >= duration:
                time -= duration
            if abs(duration - time) < (duration / 5):
                pass

        result = initialTime - time
        if result == 0.0:
            result = 0.25
        print(time, "=>", result)
        return result





    def set_duration(self,endFrame):


        minLifeTimeStrength = 0
        #minFrameLength

        match self.probabilityIsNote:
            case 0:
                print("AAAAAAAAAA")
                minLifeTimeStrength = 0.9

            case NoteProbabilities.NORMAL:
                minLifeTimeStrength = 0.45
            case NoteProbabilities.HIGH:
                minLifeTimeStrength = 0.2
        


        if np.mean(self.lifeTimeStrengths) < minLifeTimeStrength:
           print("Note failed average check")
           return False
        
        #if self.endFrame - self.startFrame

        tempo = self.processedAudioData.tempo
        frameDuration = self.processedAudioData.frameDuration

        self.start = self.snap_time_to_beat(self.startFrame * (tempo/60) * frameDuration)
        self.duration = self.snap_time_to_beat((endFrame - self.startFrame)  * (tempo/60) * frameDuration)


        debugNote = self.chroma
        if len(self.chroma) == 1:
            debugNote += " "
        
        debugNote += str(self.octave)

        UI.print_colour("{} {} {}                                   \n".format(debugNote, round(self.start,4), round(self.duration,4)),UI.CYAN)
        return True
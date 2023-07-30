import ui.UI as UI
import AudioProcessor

import math
import librosa


NOTE_DURATONS = [
    8, # Breve
    4, # Semibreve
    2, # Minim
    1, # Crotchet
    0.5, # Quaver
    0.25, # Semiquaver
  #  0.125 # Demisemiquaver

]



class Note:
    duration: float
    note: str
    octave: int

    midi: int
    start: float
    tempo: int


    startSample: int

    def __init__(self,_note,_octave,_startSample,_tempo) -> None:

        self.note = _note
        self.octave = _octave
        self.startSample = _startSample
        self.tempo = _tempo

        self.midi = librosa.note_to_midi(self.note + str(self.octave))




    def snap_time_to_grid(self,time):
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
        #print(time, "=>", result)
        return result





    def set_duration(self,endSample):

        self.start = self.snap_time_to_grid(self.startSample * AudioProcessor.pointDuration * (self.tempo/60))
        self.duration = self.snap_time_to_grid((endSample - self.startSample) * AudioProcessor.pointDuration * (self.tempo/60))


        debugNote = self.note
        if len(self.note) == 1:
            debugNote += " "
        
        debugNote += str(self.octave)

        UI.print_colour("{} {} {}\n".format(debugNote, round(self.start,4), round(self.duration,4)),UI.CYAN)
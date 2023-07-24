import ui.UI as UI
import AudioProcessor

import librosa
class Note:
    duration: int
    note: str
    octave: int

    midi: int
    start: int
    tempo: int


    startSample: int

    def __init__(self,_note,_octave,_startSample,_tempo) -> None:

        self.note = _note
        self.octave = _octave
        self.startSample = _startSample
        self.tempo = _tempo

        self.midi = librosa.note_to_midi(self.note + str(self.octave))







    def set_duration(self,endSample):

        self.start = self.startSample * AudioProcessor.pointDuration * (self.tempo/60)
        self.duration = (endSample - self.startSample) * AudioProcessor.pointDuration * (self.tempo/60)


        debugNote = self.note
        if len(self.note) == 1:
            debugNote += " "
        
        debugNote += str(self.octave)

        UI.print_colour("{} {} {}\n".format(debugNote, round(self.start,4), round(self.duration,4)),UI.CYAN)
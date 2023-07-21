import ui.UI as UI

import librosa
class Note:
    duration: int
    note: str
    octave: int

    midi: int
    start: int

    def __init__(self,_note,_octave,_start,_duration) -> None:

        self.note = _note
        self.octave = _octave
        self.start = _start
        self.duration = _duration

        self.midi = librosa.note_to_midi(self.note + str(self.octave))


        debugNote = self.note
        if len(self.note) == 1:
            debugNote += " "
        
        debugNote += str(self.octave)

        UI.print_colour("{} {} {}\n".format(debugNote, round(self.start,4), round(self.duration,4)),UI.CYAN)


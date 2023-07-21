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

        print(self.note + str(self.octave), self.start, self.duration)


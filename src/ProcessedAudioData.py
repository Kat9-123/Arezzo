from typing import NamedTuple
from numpy import array
# return (spectrum,chroma,onset,tempo,duration)

class ProcessedAudioData(NamedTuple):
    spectrum: array
    chroma: array
    onsets: array
    tempo: float
    duration: float


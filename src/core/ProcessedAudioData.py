from typing import NamedTuple
from numpy import array
# return (spectrum,chroma,onset,tempo,duration)

class ProcessedAudioData(NamedTuple):
    spectrum: array
    onsets: array
    tempo: float
    duration: float
    frameCount: int
    frameDuration: float

    loudest: float
    origTempo: float


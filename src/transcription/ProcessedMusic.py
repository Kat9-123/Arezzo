from typing import NamedTuple

class ProcessedMusic(NamedTuple):
    notes: list
    tempo: float
    key: str
    timeSig: str


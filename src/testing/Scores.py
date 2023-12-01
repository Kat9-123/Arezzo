from typing import NamedTuple

class Scores(NamedTuple):
    noteScore: float

    tempoOrig: int
    tempoGen: int
    tempoScore: float

    keyOrig: str
    keyGen: str
    keyScore: float

    timeOrig: str
    timeGen: str
    timeScore: float


    totalScore: float



from dataclasses import dataclass


DELAY_SECONDS = 0.5
HOURS_OF_LOG = 48

SECONDS_IN_MINUTE = 60
MINUTES_IN_HOUR = 60

N_SAMPLES = (SECONDS_IN_MINUTE // DELAY_SECONDS) * HOURS_OF_LOG * MINUTES_IN_HOUR


def MuTESLA2MilliGAUSS(x): return 10 * x


@dataclass
class Mag:
    x: float
    y: float
    z: float
    magnitude: float


@dataclass
class Measurement:
    time: int
    temperature: float
    mag: Mag

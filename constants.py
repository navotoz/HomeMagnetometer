from dataclasses import dataclass


DELAY_SECONDS = 0.5
HOURS_OF_LOG = 48

SECONDS_IN_MINUTE = 60
MINUTES_IN_HOUR = 60

N_SAMPLES = int((SECONDS_IN_MINUTE // DELAY_SECONDS) * HOURS_OF_LOG * MINUTES_IN_HOUR)


@dataclass
class Measurement:
    time: int
    temperature: float

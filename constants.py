PORT = 37020
DELAY_SECONDS = 0.5
HOURS_OF_LOG = 48

SECONDS_IN_MINUTE = 60
MINUTES_IN_HOUR = 60

N_SAMPLES = (SECONDS_IN_MINUTE // DELAY_SECONDS) * HOURS_OF_LOG * MINUTES_IN_HOUR

MuTESLA2MilliGAUSS = lambda x: 10 * x


class EnumData(Enum):
    TIME: auto()
    COUNTER: auto()
    TEMPERATURE: auto()
    MAG_X: auto()
    MAG_Y: auto()
    MAG_Z: auto()

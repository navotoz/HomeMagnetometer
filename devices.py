import math

import adafruit_lis3mdl
import adafruit_shtc3
import board

from constants import MuTESLA2MilliGAUSS


class Magnetometer:
    def __init__(self):
        i2c = board.I2C()
        sensor = adafruit_lis3mdl.LIS3MDL(i2c)
        sensor.data_rate = adafruit_lis3mdl.Rate.RATE_155_HZ
        sensor.performance_mode = adafruit_lis3mdl.PerformanceMode.MODE_ULTRA
        sensor.range = adafruit_lis3mdl.Range.RANGE_4_GAUSS
        self._sensor = sensor
        self._offsets = {'x': 0, 'y': 0, 'z': 235}

    def __call__(self, *args, **kwargs) -> list:
        return [MuTESLA2MilliGAUSS(v) + o for v, o in zip(self._sensor.magnetic, self._offsets.values())]

    @property
    def magnitude(self) -> float:
        return math.sqrt(sum([p ** 2 for p in self()]))


class Temperature:
    def __init__(self):
        i2c = board.I2C()
        self._sensor = adafruit_shtc3.SHTC3(i2c)

    def __call__(self, *args, **kwargs) -> float:
        return self._sensor.temperature
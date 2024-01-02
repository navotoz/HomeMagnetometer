import adafruit_shtc3
import board


class Temperature:
    def __init__(self):
        i2c = board.I2C()
        self._sensor = adafruit_shtc3.SHTC3(i2c)

    def __call__(self, *args, **kwargs) -> float:
        return self._sensor.temperature

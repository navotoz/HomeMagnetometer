from collections import deque
import threading as th
from time import sleep
from datetime import datetime

from constants import DELAY_SECONDS, N_SAMPLES,  Measurement
from devices import Temperature
from flask import Flask


def th_measurements():
    while True:
        measurement = Measurement(
            time=datetime.now().isoformat(),
            temperature=temperature(),
        )
        deque_measurements.append(measurement)
        sleep(DELAY_SECONDS)


# Create a Flask app
app = Flask(__name__)


@app.route("/", methods=["POST"])
def send_data():
    return [[p.time for p in deque_measurements], [p.temperature for p in deque_measurements]]


# Run the app
if __name__ == "__main__":
    temperature = Temperature()
    deque_measurements = deque(maxlen=N_SAMPLES)

    th_measurements_run = th.Thread(target=th_measurements, daemon=True, name='measurements')
    th_measurements_run.start()

    app.run(host="0.0.0.0", port=5000)

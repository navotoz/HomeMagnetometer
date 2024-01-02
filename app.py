from collections import deque

from time import sleep
import threading as th
from datetime import datetime

from constants import DELAY_SECONDS, N_SAMPLES,  Measurement
from devices import Temperature
import plotly.graph_objects as go
import streamlit as st


def th_measurements():
    while True:
        measurement = Measurement(
            time=datetime.now(),
            temperature=temperature(),
        )
        deque_measurements.append(measurement)
        sleep(DELAY_SECONDS)


# Create a streamlit app
st.title("Temperature measurements")


# Create a placeholder for the plot
plot = st.empty()


if __name__ == '__main__':
    temperature = Temperature()
    deque_measurements = deque(maxlen=N_SAMPLES)

    # init thread for measurements
    th_meas = th.Thread(target=th_measurements, daemon=True, name='measurements')
    th_meas.start()

    while True:
        x = [p.time for p in deque_measurements]
        y = [p.temperature for p in deque_measurements]

        # Create a Plotly figure object
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y))
        fig.update_layout(title="Temperature [C]", xaxis_title="Time", yaxis_title="Celsius")

        # Display the plot in Streamlit
        plot.plotly_chart(fig)

        sleep(DELAY_SECONDS)

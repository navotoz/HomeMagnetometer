from time import sleep

from constants import DELAY_SECONDS
import plotly.graph_objects as go
import streamlit as st
from requests import post
from datetime import datetime


# Create a streamlit app
st.title("Temperature measurements")


# Create a placeholder for the plot
plot = st.empty()


if __name__ == '__main__':
    while True:
        response = post("http://server:5000/")
        if not response.ok:
            raise Exception("Error")
        meas_time, meas_temperature = response.json()
        meas_time = [datetime.fromisoformat(t) for t in meas_time]

        # Create a Plotly figure object
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meas_time, y=meas_temperature))
        fig.update_layout(title="Temperature [C]", xaxis_title="Time", yaxis_title="Celsius")

        # Display the plot in Streamlit
        plot.plotly_chart(fig)

        sleep(DELAY_SECONDS)

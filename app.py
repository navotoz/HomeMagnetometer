from collections import deque
import qwiic_oled_display

from time import sleep
import threading as th

from constants import DELAY_SECONDS, N_SAMPLES, Mag, Measurement
from devices import Magnetometer, Temperature
import numpy as np
import pandas as pd

import dash
from dash import html, dcc
import plotly.express as px


def lcd_updater():
    myOLED = qwiic_oled_display.QwiicOledDisplay()
    if not myOLED.connected:
        raise RuntimeError("The Qwiic Micro OLED device isn't connected to the system. Please check connection")
    myOLED.begin()

    #  clear(ALL) will clear out the OLED's graphic memory.
    #  clear(PAGE) will clear the Arduino's display buffer.
    myOLED.clear(myOLED.ALL)  # Clear the display's memory (gets rid of artifacts)
    myOLED.clear(myOLED.PAGE)  # Clear the display's memory (gets rid of artifacts)
    myOLED.display()

    while True:
        myOLED.clear(myOLED.PAGE)  # Clear the display's memory (gets rid of artifacts)

        myOLED.line(x0=66, y0=0, x1=66, y1=32)

        myOLED.set_cursor(74, 0)  # Set cursor to top-middle-left
        myOLED.set_font_type(0)  # Repeat
        myOLED.print('Celsius')
        myOLED.set_cursor(74, 16)  # Set cursor to top-middle-left
        myOLED.set_font_type(1)  # Repeat
        myOLED.print(f'{temperature():2.1f}')

        myOLED.set_cursor(0, 0)  # Set cursor to top-middle-left
        myOLED.set_font_type(0)  # Repeat
        myOLED.print('Gauss')
        myOLED.set_cursor(0, 16)  # Set cursor to top-middle-left
        myOLED.set_font_type(1)  # Repeat
        myOLED.print(f'{magnetometer.magnitude:1.2f}')

        myOLED.display()

        sleep(DELAY_SECONDS)


def th_measurements():
    while True:
        mag = magnetometer()
        measurement = Measurement(
            time=magnetometer.time,
            temperature=temperature(),
            mag=Mag(
                x=mag.x,
                y=mag.y,
                z=mag.z,
                magnitude=mag.magnitude
            )
        )
        deque_measurements.append(measurement)
        sleep(DELAY_SECONDS)


app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='temperature-plot'),
    dcc.Interval(id='interval', interval=2000)
])


@app.callback(
    dash.dependencies.Output('temperature-plot', 'figure'),
    dash.dependencies.Input('interval', 'n_intervals'))
def update_graph(n_intervals):
    x = np.array([p.time for p in deque_measurements])
    y = np.array([p.temperature for p in deque_measurements])
    df = pd.DataFrame({'Time': x, 'Celsius': y})
    fig = px.line(df, x='Time', y='Celsius')
    fig.update_layout(
        title={
            'text': "Temperature [C]",
            'y': 1,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    return fig


if __name__ == '__main__':
    magnetometer = Magnetometer()
    temperature = Temperature()
    deque_measurements = deque(maxlen=N_SAMPLES)

    # init thread for measurements
    th_meas = th.Thread(target=th_measurements, daemon=True, name='measurements')
    th_meas.start()

    # init thread for LCD printing
    th_lcd = th.Thread(target=lcd_updater, daemon=True, name='lcd_updater')
    th_lcd.start()

    # init server
    PORT = 8080
    IP = "0.0.0.0"
    print('Initiating server', flush=True)
    app.run_server(debug=False, host=IP, port=PORT, threaded=True)

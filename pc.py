from time import sleep
import threading as th
import socket
import numpy as np
import pandas as pd
from tqdm import tqdm
from time import time_ns

from datetime import datetime
from constants import PORT, DELAY_SECONDS, N_SAMPLES
from collections import deque

import dash
from dash import html, dcc
import matplotlib.pyplot as plt
import plotly.express as px


app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='temperature-plot'),
    dcc.Interval(id='interval', interval=2000)
])


@app.callback(
    dash.dependencies.Output('temperature-plot', 'figure'),
    dash.dependencies.Input('interval', 'n_intervals'))
def update_graph(n_intervals):
    with lock_deque:
        indices_sort = np.argsort(deque_counter)
        x = np.array([p+time_delta for p in deque_time])[indices_sort]
        y = np.array(deque_temperature)[indices_sort]
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


def _th_reader():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    # Enable broadcasting mode
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    client.bind(("", PORT))
    while True:
        data, addr = client.recvfrom(1024)
        timestamp, counter, temperature = data.split()
        with lock_deque:
            deque_counter.append(int(counter))
            deque_time.append(datetime.fromtimestamp(float(timestamp)))
            deque_temperature.append(float(temperature))
        sleep(DELAY_SECONDS / 3)


if __name__ == '__main__':
    deque_counter = deque(maxlen=N_SAMPLES)
    deque_time = deque(maxlen=N_SAMPLES)
    deque_temperature = deque(maxlen=N_SAMPLES)
    lock_deque = th.Lock()

    th_reader = th.Thread(target=_th_reader, name='reader', daemon=True)
    th_reader.start()

    time_initial = None

    with tqdm(desc='Waiting for first sample from device') as progressbar:
        while time_initial is None:
            try:
                with lock_deque:
                    time_initial, counter_initial = deque_time[0], deque_counter[0]
                time_delta = datetime.now() - time_initial
                break
            except IndexError:
                progressbar.update()
                pass
            finally:
                sleep(1)

    PORT = 8080
    IP = "0.0.0.0"
    print('Initiating server', flush=True)
    app.run_server(debug=True, host=IP, port=PORT, threaded=True)
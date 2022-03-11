import qwiic_oled_display

from time import sleep
from datetime import datetime
import socket
import threading as th
from collections import deque

from constants import DELAY_SECONDS, PORT
from devices import Magnetometer, Temperature


def _th_send():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('0.0.0.0', 0))
    while True:
        ns, c, t, x, y, z = deque_msg[0]
        msg = f'{ns} {c} {t:2.2f} {x:g} {y:g} {z:g}'
        sock.sendto(bytes(msg, 'ascii'), ("255.255.255.255", PORT))
        print(msg)
        sleep(DELAY_SECONDS)


if __name__ == '__main__':
    magnetometer = Magnetometer()
    temperature = Temperature()
    myOLED = qwiic_oled_display.QwiicOledDisplay()
    if not myOLED.connected:
        raise RuntimeError("The Qwiic Micro OLED device isn't connected to the system. Please check connection")
    myOLED.begin()

    #  clear(ALL) will clear out the OLED's graphic memory.
    #  clear(PAGE) will clear the Arduino's display buffer.
    myOLED.clear(myOLED.ALL)  # Clear the display's memory (gets rid of artifacts)
    myOLED.clear(myOLED.PAGE)  # Clear the display's memory (gets rid of artifacts)
    myOLED.display()

    deque_msg = deque(maxlen=1)
    counter = 0
    deque_msg.append((datetime.now().timestamp(), counter, temperature(), *magnetometer()))
    counter += 1

    th_sender = th.Thread(target=_th_send, name='sender', daemon=True)
    th_sender.start()

    while True:
        t = temperature()
        deque_msg.append((datetime.now().timestamp(), counter, t, *magnetometer()))
        counter += 1

        myOLED.clear(myOLED.PAGE)  # Clear the display's memory (gets rid of artifacts)

        myOLED.line(x0=66, y0=0, x1=66, y1=32)

        myOLED.set_cursor(74, 0)  # Set cursor to top-middle-left
        myOLED.set_font_type(0)  # Repeat
        myOLED.print('Celsius')
        myOLED.set_cursor(74, 16)  # Set cursor to top-middle-left
        myOLED.set_font_type(1)  # Repeat
        myOLED.print(f'{t:2.1f}')

        myOLED.set_cursor(0, 0)  # Set cursor to top-middle-left
        myOLED.set_font_type(0)  # Repeat
        myOLED.print('Gauss')
        myOLED.set_cursor(0, 16)  # Set cursor to top-middle-left
        myOLED.set_font_type(1)  # Repeat
        myOLED.print(f'{magnetometer.magnitude * 1e-3:1.2f}')

        myOLED.display()

        sleep(DELAY_SECONDS)

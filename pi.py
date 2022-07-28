import qwiic_oled_display

from time import sleep
import threading as th

from constants import DELAY_SECONDS, PORT
from devices import Magnetometer, Temperature
from Flask import Flask
app = Flask(__name__)


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


@app.route('/temperature')
def measurements():
    return str(temperature())


@app.route('/magnetic')
def measurements():
    return '{:g} {:g} {:g}'.format(*magnetometer())


@app.route('/magnitude')
def measurements():
    return str(magnetometer.magnitude)


if __name__ == '__main__':
    magnetometer = Magnetometer()
    temperature = Temperature()

    # init thread for LCD printing
    th_lcd = th.Thread(target=lcd_updater, daemon=True, name='lcd_updater')
    th_lcd.start()

    # init server
    PORT = 8080
    IP = "0.0.0.0"
    print('Initiating server', flush=True)
    app.run_server(debug=False, host=IP, port=PORT, threaded=True)

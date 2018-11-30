import Adafruit_DHT
import RPi.GPIO as GPIO
import sys
import threading
from time import sleep
from urllib.request import urlopen


def get_sensor_data():
    threading.Timer(900.0, getSensorData).start()
    RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    print(str(T))
    print(str(RH))


print('Blah')




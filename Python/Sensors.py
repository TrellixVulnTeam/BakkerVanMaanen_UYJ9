import sys
import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT
from urllib.request import urlopen
import threading
import Bakkerbase as bb

def getSensorData():
    threading.Timer(900.0, getSensorData).start()
    RH1, T1 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    # RH2, T2 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 6)
    # RH3, T3 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 8)
    # roep firebase methode hier.
    temperature_data = [
            { 'temp_sensor_no': 1, 'temperature': T1, 'humidity': RH1 },
            { 'temp_sensor_no': 2, 'temperature': T2, 'humidity': RH2 },
            { 'temp_sensor_no': 3, 'temperature': T3, 'humidity': RH3 }
    ]
    bb.save_temperature(temperature_data)


getSensorData()

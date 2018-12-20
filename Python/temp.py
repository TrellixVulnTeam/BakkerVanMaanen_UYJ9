import RPi.GPIO as GPIO 
import Adafruit_DHT 
import Bakkerbase
import time

def getSensorData():
    RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,4)
    #Reza Toegoevoegd
    RH2, T2 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,17)
    RH3, T3 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,24) 
    temperature_data = [
		{'temp_sensor_no':1,'temperature': T,'humidity':RH},
                {'temp_sensor_no':2,'temperature': T2,'humidity':RH2},
                {'temp_sensor_no':3,'temperature': T3,'humidity':RH3}
    ]
    Bakkerbase.save_temperature(temperature_data)

while True: 
    time.sleep(300)
    getSensorData()

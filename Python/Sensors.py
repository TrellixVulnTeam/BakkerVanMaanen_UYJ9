import sys 
import RPi.GPIO as GPIO 
from time import sleep 
import Adafruit_DHT 
from urllib.request import urlopen
import threading


def getSensorData():
  threading.Timer(900.0, getSensorData).start() 
  RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,4) 
  print(str(T))
  print(str(RH))
  
     
getSensorData()  
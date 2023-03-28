#!/usr/bin/env python

import time
import grovepi
from flask import Flask
from flask import request, jsonify
from ctypes import byref

app = Flask(__name__)

# Connect the Grove Temperature Sensor to analog port A0
# SIG,NC,VCC,GND
sensor = 0
# Connect the Grove LED to digital port D4
# SIG,NC,VCC,GND
led = 4
# Connect the Grove Buzzer to digital port D8
# SIG,NC,VCC,GND
buzzer = 8

#Port setup
#grovepi.pinMode(sensor,"INPUT")
grovepi.pinMode(led,"OUTPUT")
grovepi.pinMode(buzzer,"OUTPUT")

#Default values of optimal and max temperature
optimal_temperature = 20
max_temperature = 30
temp = 0
led_on = False
buzzer_on = False

def setPins(temp):
    global led_on
    global buzzer_on
    
    if temp > optimal_temperature:
        grovepi.digitalWrite(led,1)
        led_on = True
    else: #temp < optimal_temperature:
        grovepi.digitalWrite(led,0)
        led_on = False
        
    if temp > max_temperature:
        grovepi.digitalWrite(buzzer,1)
        buzzer_on = True
    else: #temp < max_temperature:
        grovepi.digitalWrite(buzzer,0)
        buzzer_on = False
        
    return 0

@app.route("/")
def hello():
    return "Hello World"

@app.route('/api/sensores/temperature' ,methods=['GET'])
def getTemp():
    global temp
    try:
        temp = grovepi.temp(sensor,'1.1')
        
        setPins(temp)
        
        return jsonify( {"Current temperature": temp, "Optimal temperature": optimal_temperature,"Max Temperature": max_temperature})
    except (IOError, TypeError) as e:
        return jsonify({"error": e})

@app.route('/api/sensores/temperature' ,methods=['PUT'])
def setTemp():
    global temp
    global optimal_temperature
    global max_temperature
    try:
        optimal_temperature = request.json['optimal_temperature']
        max_temperature = request.json['max_temperature']
        
        temp = grovepi.temp(sensor,'1.1')
        
        setPins(temp)
            
        return jsonify( {"Optimal temperature": optimal_temperature,"Max Temperature": max_temperature})
    except (IOError, TypeError) as e:
        return jsonify({"error": e})

@app.route('/api/actuadores/led' ,methods=['GET'])
def getLed():
    try:
        return jsonify( {"Led on": led_on})
    except (IOError, TypeError) as e:
        return jsonify({"error": e})
    
@app.route('/api/actuadores/buzzer' ,methods=['GET'])
def getBuzzer():
    try:
        return jsonify( {"Buzzer on": buzzer_on})
    except (IOError, TypeError) as e:
        return jsonify({"error": e})

if __name__ =="__main__":
    app.run(host="0.0.0.0", port = 5000)

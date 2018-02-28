#!/usr/bin/env python

"""Imports"""
import os
import socket
import threading
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send

# Get environment variable indicating testing or on device.
env = os.getenv('PYTHON_ENV', 'production')
print('Running in ' + env + ' mode.')

# Conditional import based on above environment variable.
if env == 'production':
  import Adafruit_DHT # https://github.com/adafruit/Adafruit_Python_DHT
else:
  from random import *

# Globals that hold the latest temp and humidity data.
lastTempRead = 0
lastHumidityRead = 0

def readFromSensor():
  """
  Perform a sensor read and store the values in the
  global variables lastTempRead and lastHumidityRead respectively.
  """
  global lastTempRead
  global lastHumidityRead
  global env
  if env != 'production':
    lastTempRead = random()
    lastHumidityRead = random()
  else:
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    if humidity is not None and temperature is not None:
      lastTempRead = temperature
      lastHumidityRead = humidity

def getIP():
  """
  Get the IP of the server so we can pass it to index.html
  when we render it. This means I don't have to change the IP
  address in index.html and redeploy if the IP of the server
  changes.
  """
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    s.connect(('10.255.255.255', 1))
    IP = s.getsockname()[0]
  except:
    IP = '127.0.0.1'
  finally:
    s.close()
  return IP

def setInterval(func, sec):
  """
  Allows me to perform the read and emit data at set time intervals and
  separate from eachother.
  """
  def func_wrapper():
    setInterval(func, sec)
    func()
  t = threading.Timer(sec, func_wrapper)
  t.start()
  return t

def emitData():
  """
  Emit the latest data read to all the open sockets.
  """
  socketio.emit('data', {'temperature': lastTempRead, 'humidity': lastHumidityRead}, broadcast = True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# App Routes
@app.route('/')
def root():
  """
  Render the templates/index.html file.
  """
  ipAddr = getIP()
  return render_template('index.html', ipAddr = ipAddr + ':5000')

@app.route('/favicon.ico')
def favicon():
  """
  Render the favicon file.
  """
  return app.send_static_file('favicon.ico')

socketio = SocketIO(app, async_mode='threading')

@socketio.on('connected')
def connected():
    """
    Enable us to emit the latest sensor data we read to a new client
    when they first connect. No need to read the sensor again.
    """
    socketio.emit('data', {'temperature': lastTempRead, 'humidity': lastHumidityRead})

if __name__ == '__main__':
  readFromSensor()
  setInterval(emitData, 15)
  """
  If we read too often the sensor heats up and throws off the data
  or it will simply hang. We don't even really need data this often
  because the reading rarely changes in this time span under my usage
  scenario.
  """
  setInterval(readFromSensor, 30)
  socketio.run(app, '0.0.0.0')



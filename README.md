# Pi Temp and Humidity Sensor

IoT DHT22 Live Monitoring for Raspberry Pi.

Had a few challenges developing this. At first I had the app reading from the DHT22 every 5 seconds for every connected person. This would cause the device itself to heat up and prevent the accurate measurement of the tempurature. I solved this issue by setting the read from the device to happen once time every 30 seconds and I emit that stored value to all users at once, via sockets, every 15 seconds. This prevents any heating issues and gives accurate measurements.

1. Install Adafruit_DHT
  - https://github.com/adafruit/Adafruit_Python_DHT
2. pip install -r requirements.txt
3. python main.py
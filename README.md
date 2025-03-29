# Pi Temp and Humidity Sensor

A Flask-based IoT application for live monitoring of temperature and humidity using a DHT22 sensor on a Raspberry Pi. The application serves an HTML page that updates every 15 seconds via WebSockets to display the current temperature and humidity.

## Features
- Real-time temperature and humidity updates using Flask-SocketIO.
- Optimized sensor reading to prevent overheating and ensure accurate measurements.
- Automatically detects and uses the server's IP address for client connections.

## Installation

1. **Install Adafruit_DHT library**  
   Follow the instructions at [Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT) to install the library.

2. **Install Python dependencies**  
   Run the following command to install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**  
   Start the application with:
   ```bash
   python main.py
   ```

## How It Works
- The server reads data from the DHT22 sensor every 30 seconds to avoid overheating the sensor.
- The latest sensor data is broadcast to all connected clients every 15 seconds using WebSockets.
- The HTML page dynamically updates the displayed temperature and humidity values without requiring a page refresh.

## File Structure
```
.
├── .gitignore
├── main.py                   # Main application script
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── static/
│   ├── favicon.ico           # Favicon for the web page
├── templates/
│   ├── index.html            # HTML template for the web page
```

## Notes
- Ensure the `PYTHON_ENV` environment variable is set to `production` when running on the Raspberry Pi to enable sensor readings. In other environments, random values will be used for testing.
- The server's IP address is automatically passed to the client, so no manual configuration is needed if the IP changes.

## Troubleshooting
- If the sensor readings are incorrect or the application hangs, ensure the DHT22 sensor is connected properly and the Adafruit_DHT library is installed correctly.
- For development or testing, set `PYTHON_ENV` to any value other than `production` to simulate sensor readings with random values.

## License
This project is licensed under the MIT License.


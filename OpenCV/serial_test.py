from flask import Flask, request
from flask_cors import CORS
import smbus  # For I2C communication
import threading
import RPi.GPIO as GPIO
import time

GPIO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.OUT)
try:
    GPIO.output(GPIO_PIN, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(GPIO_PIN, GPIO.HIGH)
finally:
    GPIO.cleanup()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# I2C settings
I2C_BUS = 1               # For Raspberry Pi, the I2C bus is typically 1
I2C_SLAVE_ADDR = 0x08     # I2C slave address of the ESP32-S3

# Initialize the I2C bus
try:
    bus = smbus.SMBus(I2C_BUS)
    print("I2C bus initialized successfully")
except Exception as e:
    print(f"Failed to initialize I2C bus: {e}")
    bus = None

def send_to_i2c(data):
    """Send data to the ESP via I2C."""
    global bus
    if bus:
        try:
            # Convert the string data to a list of byte values
            byte_data = [ord(c) for c in data]
            # Send the data as a block
            bus.write_i2c_block_data(I2C_SLAVE_ADDR, 0x00, byte_data[:32])  # 0x00 is the command/register address
            print(f"Sent to ESP via I2C: {data}")
        except Exception as e:
            print(f"Error sending to ESP via I2C: {e}")
    else:
        print("I2C bus is not available")

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json  # Parse JSON data from the request
    if data:
        # Extract and concatenate the values
        vertical = data.get('vertical', '')
        horizontal = data.get('horizontal', '')
        combined_data = f"{vertical}{horizontal}"  # Concatenate values
        print(f"Received data: {combined_data}")

        # Start a new thread to send data to the ESP via I2C
        threading.Thread(target=send_to_i2c, args=(combined_data,), daemon=True).start()
        return {"status": "success", "received": combined_data}, 200
    else:
        return {"status": "error", "message": "No data received"}, 400

if __name__ == '__main__':
    try:
        # Start the Flask app
        app.run(host='0.0.0.0', port=5000, threaded=True)  # Allow multithreaded requests
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Flask app stopped")

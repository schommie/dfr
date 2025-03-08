import machine
import time
import ustruct

# I2C Setup (Master)
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=100000)

# Slave Address for Pico2W.2 (Temperature Sensor)
temp_address = 0x11

# LED Setup
led = machine.Pin("LED", machine.Pin.OUT)

# Read from I2C Slave
def read_sensor(address):
    buffer = bytearray(2)
    try:
        i2c.readfrom_into(address, buffer)  # Request data
        return ustruct.unpack(">H", buffer)[0]  # Convert bytes to int
    except OSError:
        return None  # If no response

while True:
    # Blink LED to show data is being received
    led.toggle()

    # Request data from Pico2W.2 (Temperature Slave)
    temp_humidity = read_sensor(temp_address)

    if temp_humidity:
        temp = (temp_humidity >> 8) & 0xFF  # Extract temperature
        humidity = temp_humidity & 0xFF  # Extract humidity
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")
    else:
        print("No response from Pico2W.2")

    time.sleep(1)

import machine
import dht
import ustruct
import utime

# I2C Setup - Pico2W.2 as Slave (Address: 0x11)
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=100000)
slave_address = 0x11  # Unique I2C address for this slave

# DHT11 Sensor Setup
sensor = dht.DHT11(machine.Pin(16))  # GPIO 16
buffer = bytearray(2)  # 2-byte buffer for data (temperature + humidity)

print("Pico2W.2 (I2C Slave) Ready...")

def update_sensor():
    try:
        sensor.measure()  # Read DHT11
        temp = sensor.temperature()  # Get temperature (°C)
        humidity = sensor.humidity()  # Get humidity (%)
        value = (temp << 8) | humidity  # Pack temp and humidity into 2 bytes
        ustruct.pack_into(">H", buffer, 0, value)  # Convert to bytes
    except OSError:
        print("DHT11 read error")
    utime.sleep(2)

while True:
    update_sensor()  # Continuously read sensor data
    try:
        i2c.writeto(slave_address, buffer)  # Send data when requested
    except OSError:
        pass  # Ignore errors when master isn't requesting
    utime.sleep(1)

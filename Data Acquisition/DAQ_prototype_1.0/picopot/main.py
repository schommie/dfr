import machine
import utime
import ustruct
import time

led = machine.Pin("LED", machine.Pin.OUT)

while True:
    led.toggle()  # Blink LED
    time.sleep(1)  # 1-second delay

# I2C Setup - Pico2W.1 as Slave
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=100000)
slave_address = 0x10  # Unique I2C address for this device

pot = machine.ADC(26)  # Potentiometer on GPIO 26
buffer = bytearray(2)  # 2-byte buffer for data

print("Pico2W.1 (I2C Slave) Ready...")

while True:
    value = pot.read_u16()  # Read potentiometer (0-65535)
    ustruct.pack_into(">H", buffer, 0, value)  # Convert to 2-byte format

    try:
        i2c.writeto(slave_address, buffer)  # Send to master when requested
    except OSError:
        pass  # Ignore errors if master isn’t requesting

    utime.sleep(0.1)  # Small delay to avoid flooding I2C

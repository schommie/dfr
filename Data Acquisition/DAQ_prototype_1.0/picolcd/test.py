import machine

i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=100000)

devices = i2c.scan()

if devices:
    print("I2C Devices Found at:", [hex(device) for device in devices])
else:
    print("No I2C devices found! Check wiring.")

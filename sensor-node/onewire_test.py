# Simple demo of printing the temperature from the first found DS18x20 sensor every second.
# Author: Tony DiCola
import time

import board

from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20


# Initialize one-wire bus on board pin D5.
ow_bus = OneWireBus(board.D5)

# Scan for sensors and grab the first one found.
ds18_bus=ow_bus.scan()
print(ds18_bus)

ds18=[]
for probe in ds18_bus:
    print(probe)
    ds18.append(DS18X20(ow_bus, probe))

# Main loop to print the temperature every second.
while True:

    for sensor in ds18:
        print('Temperature: {0:0.3f}C'.format(sensor.temperature))
        time.sleep(1.0)

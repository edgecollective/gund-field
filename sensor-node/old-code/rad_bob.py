# CircuitPython Demo - USB/Serial echo

import board
import busio
import digitalio
import time
import adafruit_rfm9x

# lora radio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.RFM9X_CS)
reset = digitalio.DigitalInOut(board.RFM9X_RST)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)

# led
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT


while True:
    
    #print("Listening ...")
    
    packet = rfm9x.receive()  # Wait for a packet to be received (up to 0.5 seconds)
    if packet is not None:
        packet_text = str(packet, 'ascii')
        #print('Received: {0}'.format(packet_text))
        #print("Received: "+packet_text)
        print(packet_text)
        led.value=True
        time.sleep(.1)
        led.value = False
        time.sleep(.1)
    

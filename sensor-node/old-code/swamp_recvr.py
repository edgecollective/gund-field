# CircuitPython Demo - USB/Serial echo

import board
import busio
import digitalio
import time
import adafruit_rfm9x
import gc

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
    
    packet = rfm9x.receive(timeout=2.)  # Wait for a packet to be received (up to 0.5 seconds)
    print(packet)
    if packet is not None:
        try:
	    packet_text = str(packet, 'ascii')
            print(packet_text)
            led.value=True
            time.sleep(.1)
            led.value = False
            time.sleep(.1)
	except exception as e:
            print(e)

    gc.collect()    


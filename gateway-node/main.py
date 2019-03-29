import ujson as json
import urequests as requests
import time
import gc
import machine
from machine import Pin
from machine import SPI
from upy_rfm9x import RFM9x
import ssd1306
from machine import I2C

TIMEOUT = 1.
DISPLAY = True
OLED_LINESKIP=18
OLED_CURRENTLINE=0

feet_per_meter=3.28084

# set up the display
i2c = I2C(-1, Pin(14), Pin(2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# set up the 'done' pin
done_pin=Pin(22,Pin.OUT)
done_pin.value(0)

# indicate that we're starting up
oled.fill(0)
oled.text("Starting up ...",0,0)
oled.show()


# radio test
sck=Pin(25)
mosi=Pin(33)
miso=Pin(32)
cs = Pin(26, Pin.OUT)
#reset=Pin(13)
led = Pin(13,Pin.OUT)

resetNum=27

spi=SPI(1,baudrate=5000000,sck=sck,mosi=mosi,miso=miso)

rfm9x = RFM9x(spi, cs, resetNum, 915.0)


# set up FARMOS params
base_url='https://wolfesneck.farmos.net/farm/sensor/listener/'
public_key='4c405092bdae34790e2ba6579d79c6ca'
private_key='a925fcb9ed71ae759b422666e1527816'
url = base_url+public_key+'?private_key='+private_key
headers = {'Content-type':'application/json', 'Accept':'application/json'}

# wifi parameters
#WIFI_NET = 'Artisan\'s Asylum'
#WIFI_PASSWORD = 'I won\'t download stuff that will get us in legal trouble.'

WIFI_NET = 'WATERBEAR-iPhone'
WIFI_PASSWORD = 'solarpunk'

# function for posting data
def post_data():
    try:
        r = requests.post(url,data=json.dumps(payload),headers=headers)
    except Exception as e:
        print(e)
        return "timeout"
    else:
        r.close()
        print('Status', r.status_code)
        return "posted"

# function for connecting to wifi
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)	
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(False)
        sta_if.active(True)
        sta_if.connect(WIFI_NET, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

index=0

# main loop

do_connect()

while True:
    
    rfm9x.receive(timeout=TIMEOUT)
    if rfm9x.packet is not None:
        try:
            packet_text = str(rfm9x.packet, 'ascii')
            rssi=str(rfm9x.rssi)
            oled.fill(0)
            #oled.text("<--",0,0)
            #oled.text(packet_text,0,30)
            oled.text("---- UVM GUND ----",0,0)
            oled.text(" radio:"+rssi,0,10)
            oled.show() 
            print('Received: {}'.format(packet_text))
            print("RSSI: {}".format(rssi))
                      
            s=packet_text.split(',')
            print(s)
            if (len(s)==4):
            
                # dielectric
                raw_dielectric=float(s[0])
                dielectric=raw_dielectric/50.

                # ec
                raw_ec=float(s[1])

                if (raw_ec>700):
                    raw_ec=5*(raw_ec-700)+700
                ec=raw_ec/100.

                # temp
                raw_temp=float(s[2])
                if (raw_temp>900):
                    raw_temp=5*(raw_temp-900)+900
                temp=(raw_temp-400)/10.
                
                # onewire
                onewire_one=float(s[3])
                
                
            payload ={"dielectric":str(dielectric),"ec":str(ec),"temp":str(temp),"onewire_one":str(onewire_one)}
            print(payload)
            oled.text("dielectric:"+str(dielectric),0,20)
            oled.text("ec:"+str(ec),0,30)
            oled.text("temp:"+str(temp),0,40)
            post_data()
            
            oled.text("Posted to FarmOS."+str(s[2]),0,50)
            oled.show() 
            time.sleep(60)
      
            
        except Exception as e:
            print(e)
            print(rfm9x.packet)

    gc.collect()
    


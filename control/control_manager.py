import Adafruit_DHT
import time

SENSOR_LOCATION_NAME = "SERVER"
BUCKET_NAME = 'Server Room Temperatures'
BUCKET_KEY = 'rt0129'
MINUTES_BETWEEN_READS = 0.5
METRICS_UNITS = False

def control_manager():

    while True:
        humidity, temp_c = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)

        if(METRICS_UNITS):
            print(SENSOR_LOCATION_NAME + " Temperature(C)", temp_c)
        else:
            temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
            print(temp_f)
        
        time.sleep(60*MINUTES_BETWEEN_READS)
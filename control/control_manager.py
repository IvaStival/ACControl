# import Adafruit_DHT
import time
import yaml

from sensors.temperature.controlDHT22 import controlDHT22

SENSOR_LOCATION_NAME = "SERVER"
BUCKET_NAME = 'Server Room Temperatures'
BUCKET_KEY = 'rt0129'
MINUTES_BETWEEN_READS = 0.5
METRICS_UNITS = True


def control_manager():

    with open('./config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    print(config)

    sensor_DHT22_01 = controlDHT22(12, 12, 1)
    # while True:
    #     humidity, temp_c = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)

    #     if(METRICS_UNITS):
    #         print(SENSOR_LOCATION_NAME + " Temperature(C)", temp_c)
    #         print(SENSOR_LOCATION_NAME + " Humidity", humidity)
    #     else:
    #         temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
    #         print(temp_f)

    #     time.sleep(60*MINUTES_BETWEEN_READS)

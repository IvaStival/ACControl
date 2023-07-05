# import yaml


class controlDHT22:
    def __init__(self, minutes_between_reads, port, unit) -> None:
        self.min = minutes_between_reads
        self.port = port
        self.unit = unit

        print(self.min, self.port, self.unit)

    # def run():
        # while True:
    #     humidity, temp_c = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)

    #     if(METRICS_UNITS):
    #         print(SENSOR_LOCATION_NAME + " Temperature(C)", temp_c)
    #         print(SENSOR_LOCATION_NAME + " Humidity", humidity)
    #     else:
    #         temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
    #         print(temp_f)

    #     time.sleep(60*MINUTES_BETWEEN_READS)

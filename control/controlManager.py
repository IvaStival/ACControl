import time
import yaml

from sensors.temperature.controlDHT22 import controlDHT22
from lcd.controlLCD import controlLCD


class controlManager:
    def __init__(self):

        with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        #### TEMPERATURE CONFIG DATA ####
        self.serve_name = config["SERVER"]["SENSOR_LOCATION_NAME"]
        self.debug = config["SERVER"]["DEBUG"]

        self.temperature_server_name = config["TEMPERATURE_SERVER"]['NAME']
        self.minutes_between_reads = config["TEMPERATURE_SERVER"]["MINUTES_BETWEEN_READS"]
        self.unit_type = config["TEMPERATURE_SERVER"]["METRICS_UNIT"]

        self.dh22_01_name = config["TEMPERATURE_SENSOR_01"]["NAME"]
        self.dh22_02_name = config["TEMPERATURE_SENSOR_02"]["NAME"]

        self.dh22_01_port = config["TEMPERATURE_SENSOR_01"]["PORT"]
        self.dh22_02_port = config["TEMPERATURE_SENSOR_02"]["PORT"]

        self.sensor_DHT22_01 = controlDHT22(
            self.dh22_01_port, self.unit_type, self.dh22_01_name, self.debug)

        #### LCD CONFIG DATA ####
        pin_rs = config["LCD"]["PIN_RS"]
        pin_e = config["LCD"]["PIN_E"]
        pins_data = config["LCD"]["PINS_DATA"]

        # INITIALIZE LCD CONTROL
        self.lcd_control = controlLCD(pin_rs, pin_e, pins_data)

        if (self.debug):
            print(self.serve_name)

    def run(self):
        result = {}
        while True:
            if (self.debug):
                print(self.temperature_server_name)

            result[self.dh22_01_name] = self.sensor_DHT22_01.run()
            print(result)
            print(60*self.minutes_between_reads)
            # time.sleep(60*minutes_between_reads)

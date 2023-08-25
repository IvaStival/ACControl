import time
import yaml

from .sensorsControl import sensorControl
from .screenControl import screenControl
from sensors.temperature.controlDHT22 import controlDHT22



class controlManager:
    def __init__(self):
        self.sensors_control = sensorControl()
        self.screen_control = screenControl()

        with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        self.serve_name = config["SERVER"]["SENSOR_LOCATION_NAME"]
        self.debug = config["SERVER"]["DEBUG"]

        self.temperature_server_name = config["TEMPERATURE_SERVER"]['NAME']
        self.minutes_between_reads = config["TEMPERATURE_SERVER"]["MINUTES_BETWEEN_READS"]
        


        

    def run(self):
        while True:
        
            self.sensors_control.run()
            self.screen_control.run()
            # self.lcd_control.write([f"T1:{t1}"], [f"H1:{h1}"])

            # TIME OUT
            time.sleep(60*self.minutes_between_reads)

import yaml
import time

from sensors.temperature.controlDHT22 import controlDHT22
from db.dbCommands import dbCommands

class sensorControl:
    def __init__(self):

        with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        #### TEMPERATURE CONFIG DATA ####
        self.unit_type = config["TEMPERATURE_SERVER"]["METRICS_UNIT"]
        self.minutes_between_reads = config["TEMPERATURE_SERVER"]["MINUTES_BETWEEN_READS"]
        
        self.dh22_01_name = config["TEMPERATURE_SENSOR_01"]["NAME"]
        self.dh22_02_name = config["TEMPERATURE_SENSOR_02"]["NAME"]

        self.dh22_01_port = config["TEMPERATURE_SENSOR_01"]["PORT"]
        self.dh22_02_port = config["TEMPERATURE_SENSOR_02"]["PORT"]

        self.debug_s1 = config["TEMPERATURE_SENSOR_01"]["DEBUG"]
        self.debug_s2 = config["TEMPERATURE_SENSOR_02"]["DEBUG"]

        self.sensor_DHT22_01 = controlDHT22(
            self.dh22_01_port, self.unit_type, self.dh22_01_name, self.debug_s1)

        self.sensor_DHT22_02 = controlDHT22(
            self.dh22_02_port, self.unit_type, self.dh22_02_name, self.debug_s2)
        
        #### DB CONFIG DATA ####
        self.user = config["DB"]["USER"]
        self.password = config["DB"]["PASSWORD"]
        self.host = config["DB"]["HOST"]
        self.port = config["DB"]["PORT"]
        self.db_name = config["DB"]["DBNAME"]

        self.db_command = dbCommands(self.user, self.password, self.host, self.port, self.db_name)

        # CREATE TABLE IF DOESN'T EXISTS
        self.db_command.createTable()

    def run(self):
        while True:
            result = {}
            result[self.dh22_01_name] = self.sensor_DHT22_01.run()
            result[self.dh22_02_name] = self.sensor_DHT22_02.run()

            # GET TEMPERATURE AND HUMIDITY OF SENSOR 1
            temp1 = result[self.dh22_01_name]['temperature']
            hum1 = result[self.dh22_01_name]['humidity']

            temp2 = result[self.dh22_02_name]['temperature']
            hum2 = result[self.dh22_02_name]['humidity']

            

            # SAVE DATA
            self.db_command.insert(s1=self.dh22_01_name, t1=temp1, h1=hum1, s2=self.dh22_02_name, t2=temp2, h2=hum2)            
            
            # TIME OUT
            time.sleep(60*self.minutes_between_reads)
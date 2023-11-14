import yaml
import time

from sensors.temperature.controlDHT22 import controlDHT22
from db.dbCommands import dbCommands

class sensorControl:
    def __init__(self):
        self.sensor_instances = []

        with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        #### TEMPERATURE CONFIG DATA ####
        self.unit_type = config["TEMPERATURE_SERVER"]["METRICS_UNIT"]
        self.minutes_between_reads = config["TEMPERATURE_SERVER"]["MINUTES_BETWEEN_READS"]
        
        self.sensor_list = config["SENSORS"]["TEMPERATURE_SENSOR"]
        
        # INITIALIZE SENSORS CONTROL
        for sensor in self.sensor_list:
            instance = controlDHT22(sensor["PORT"], self.unit_type, sensor["NAME"], sensor["DEBUG"])
            self.sensor_instances.append(instance)

        # DB CONNECTION
        self.db_command = dbCommands()

        # CREATE TABLE IF DOESN'T EXISTS
        self.db_command.createTable()

    def run(self):
        while True:
            result = {}
            count = 1
            for instance in self.sensor_instances:
                result_temp = instance.run()

                result[f"s{count}"] = result_temp["name"]
                result[f"t{count}"] = result_temp["temperature"]
                result[f"h{count}"] = result_temp["humidity"]

                count += 1


            # SAVE DATA
            self.db_command.insert(result)
            
            # TIME OUT
            time.sleep(60*self.minutes_between_reads)
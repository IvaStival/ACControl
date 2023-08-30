import yaml
import time

from db.dbCommands import dbCommands
from security.temperatureSystem import temperatureSystem
from utils.statusCode import statusCode

class securityControl:
    def __init__(self):
        self.temp_list = []

        with open('./config/config.yaml', 'r') as file:
                config = yaml.safe_load(file)

        self.debug = config["SERVER"]["DEBUG"]

        #### DB CONFIG DATA ####
        user = config["DB"]["USER"]
        password = config["DB"]["PASSWORD"]
        host = config["DB"]["HOST"]
        port = config["DB"]["PORT"]
        db_name = config["DB"]["DBNAME"]

        self.db_command = dbCommands(user, password, host, port, db_name)

        self.tempSystem = temperatureSystem(self.db_command)

    def run(self):
         while True:
            result = self.tempSystem.temperatureCheck()

        
            for (sensor_name, status_code) in result:
                if status_code == statusCode.OK_WAINTING:
                    if(self.debug):
                        print(f"[CODE {status_code}] {sensor_name} - Waiting for more data")
                
                elif status_code == statusCode.TEMPERATURE_SENSOR_ERROR:
                    if(self.debug):
                        print(f"[CODE {status_code}] {sensor_name} - Temperature Sensor Error. Data can't be readed.")

                elif status_code == statusCode.WARNING_TEMPERATURE:
                    if(self.debug):
                        print(f"[CODE {status_code}] {sensor_name} - WARNING! Temperature is HIGH.") 
                
                elif status_code == statusCode.DANGER_TEMPERATURE:
                    if(self.debug):
                        print(f"[CODE {status_code}] {sensor_name} - DANGER! Temperature is VERY HIGH.")
                elif status_code == statusCode.SENSOR_OK:
                    if(self.debug):
                        print(f"[CODE {status_code}] {sensor_name} - Sensor is OK!")

            ## TODO
            ## VOLTAGE SENSOR CHECK
            # if result == statusCode.VOLTAGE_SENSOR_ERROR:
            #     print(f"[CODE {statusCode.VOLTAGE_SENSOR_ERROR}] Voltage Sensor Error. Data can't be readed.")

            time.sleep(10)
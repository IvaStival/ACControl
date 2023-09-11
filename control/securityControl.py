import yaml
import time

from db.dbCommands import dbCommands
from security.temperatureSystem import temperatureSystem
from utils.statusCode import statusCode
from utils.piGPIOSystem import piGPIOSystem

class securityControl:
    def __init__(self):
        

        with open('./config/config.yaml', 'r') as file:
                config = yaml.safe_load(file)

        self.debug = config["SERVER"]["DEBUG"]

        n_sensors = len(config['SENSORS']['TEMPERATURE_SENSOR'])

        #### DB CONFIG DATA ####
        user = config["DB"]["USER"]
        password = config["DB"]["PASSWORD"]
        host = config["DB"]["HOST"]
        port = config["DB"]["PORT"]
        db_name = config["DB"]["DBNAME"]

        self.sensor_alert_list = [0] * n_sensors
        self.temp_warning_list = [0] * n_sensors
        self.temp_danger_list = [0] * n_sensors

        self.db_command = dbCommands(user, password, host, port, db_name)

        ### TEMPERATURE SYSTEM INIT ##
        self.tempSystem = temperatureSystem(self.db_command)

        ### GPIO SYSTEM INIT ###
        self.gpio_command = piGPIOSystem()

    def run(self):
         while True:
            result = self.tempSystem.temperatureCheck()
        
            for id, (sensor_name, status_code) in enumerate(result):
                if status_code == statusCode.OK_WAINTING:
                    if(self.debug):
                        print(f"[CODE {status_code}] {sensor_name} - Waiting for more data")
                
                if status_code == statusCode.TEMPERATURE_SENSOR_ERROR:
                    # self.gpio_command.turnOnTempSensorWarning()
                    self.sensor_alert_list[id] = 1
                    if(self.debug):
                        print(f"[CODE {status_code}] {sensor_name} - Temperature Sensor Error. Data can't be readed.")
                else:
                    # self.gpio_command.turnOffTempSensorWarning()
                    self.sensor_alert_list[id] = 0

                if status_code == statusCode.WARNING_TEMPERATURE:
                    # self.gpio_command.turnOnTempWarning()
                    self.temp_warning_list[id] = 1
                    if(self.debug):
                        print(f"[CODE {status_code}] {sensor_name} - WARNING! Temperature is HIGH.") 
                
                elif status_code == statusCode.DANGER_TEMPERATURE:
                    # self.gpio_command.turnOnTempDanger()
                    self.temp_danger_list[id] = 1
                    if(self.debug):
                        print(f"[CODE {status_code}] {sensor_name} - DANGER! Temperature is VERY HIGH.")
                elif status_code == statusCode.SENSOR_OK:
                    self.sensor_alert_list[id] = 0
                    self.temp_warning_list[id] = 0
                    self.temp_danger_list[id] = 0
                    
                    
                    if(self.debug):
                        print(f"[CODE {status_code}] {sensor_name} - Sensor is OK!")

            if(sum(self.sensor_alert_list)):
                self.gpio_command.turnOnTempSensorWarning()
            else:
                self.gpio_command.turnOffTempSensorWarning()

            if(sum(self.temp_warning_list)):
                self.gpio_command.turnOnTempWarning()
            else:
                self.gpio_command.turnOffTempWarning()

            if(sum(self.temp_danger_list)):
                self.gpio_command.turnOnTempDanger()
            else:
                self.gpio_command.turnOffTempDanger()
            
            if(not sum(self.sensor_alert_list) and not sum(self.temp_warning_list) and not sum(self.temp_danger_list)):
                self.gpio_command.turnOnOkAlert()
            else:
                self.gpio_command.turnOffOkAlert()
            ## TODO
            ## VOLTAGE SENSOR CHECK
            # if result == statusCode.VOLTAGE_SENSOR_ERROR:
            #     print(f"[CODE {statusCode.VOLTAGE_SENSOR_ERROR}] Voltage Sensor Error. Data can't be readed.")

            time.sleep(10)
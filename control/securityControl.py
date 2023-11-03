import yaml
import time

from db.dbCommands import dbCommands
from security.TemperatureSystem import TemperatureSystem
from security.ExternalComunicationSystem import ExternalComunicationSystem
from utils.statusCode import statusCode
from utils.piGPIOSystem import piGPIOSystem

import RPi.GPIO as GPIO

WARNING = 1
DANGER = 2

class securityControl:
    def __init__(self):
        with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        self.debug = config["SERVER"]["DEBUG"]

        n_sensors = len(config['SENSORS']['TEMPERATURE_SENSOR'])

        GPIO.setmode(GPIO.BCM)

        #### DB CONFIG DATA ####
        user = config["DB"]["USER"]
        password = config["DB"]["PASSWORD"]
        host = config["DB"]["HOST"]
        port = config["DB"]["PORT"]
        db_name = config["DB"]["DBNAME"]
        
        ## ----------------- SECURITY CONTROL VARIABLES --------------------
        ### ARRAY USED TO ENABLE ALERT SYSTEM TO TURN ON GPIOS AND SEND MESSAGE ALERT
        self.sensor_alert_list = [0] * n_sensors
        self.temp_warning_list = [0] * n_sensors
        self.temp_danger_list = [0] * n_sensors

        ### VARIABLE TO CONTROL EXTERNAL ALERT MESSAGES
        self.sensor_problem_message = config["TELEGRAM"]["SENSOR_PROBLEM_MESSAGE"]
        self.temperature_warning_message = config["TELEGRAM"]["TEMPERATURE_WARNING_MESSAGE"]
        self.temperature_danger_message = config["TELEGRAM"]["TEMPERATURE_DANGER_MESSAGE"]

        self.send_alert_message = False
        self.alert_message = ""
        self.sent_alert_message_time = 9999999999

        self.message_queue = []
        ## -----------------------------------------------------------------

        ### DATA BASE ACCESS CLASS ###
        self.db_command = dbCommands(user, password, host, port, db_name)

        ### TEMPERATURE SYSTEM ###
        self.tempSystem = TemperatureSystem(self.db_command)

        ### GPIO SYSTEM INIT ###
        self.gpio_command = piGPIOSystem()

        ### EXTERNAL COMUNICATION SYSTEM ###
        self.comunication = ExternalComunicationSystem()

    def alertMessageControl(self):
        if(self.send_alert_message):
            current_time = time.time()
            elapsed_time_in_min = int((current_time - self.sent_alert_message_time)/60)

            if(elapsed_time_in_min >= 5 or elapsed_time_in_min < 0):
                while len(self.message_queue):
                    
                    message = self.message_queue.pop()
                    if(message[0] == WARNING):
                        if(self.debug):
                            print("[ALERT] - Send external WARNING alert")
                        self.comunication.warningMessage(message[1])
                    if(message[0] == DANGER):
                        if(self.debug):
                            print("[ALERT] - Send external DANGER alert")
                        self.comunication.dangerMessage(message[1])
                    time.sleep(1)
                
                self.sent_alert_message_time = time.time()

    def run(self):
         while True:
            result = self.tempSystem.temperatureCheck()
            self.message_queue = []

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
                self.send_alert_message = True
                self.message_queue.append([WARNING, self.sensor_problem_message])
            else:
                self.gpio_command.turnOffTempSensorWarning()

            if(sum(self.temp_warning_list)):
                self.send_alert_message = True
                self.gpio_command.turnOnTempWarning()
                self.message_queue.append([WARNING, self.temperature_warning_message])
            else:
                self.gpio_command.turnOffTempWarning()

            if(sum(self.temp_danger_list)):
                self.send_alert_message = True
                self.gpio_command.turnOnTempDanger()
                self.message_queue.append([DANGER, self.temperature_danger_message])
            else:
                self.gpio_command.turnOffTempDanger()

            ## TODO
            ## VOLTAGE SENSOR CHECK
            # if result == statusCode.VOLTAGE_SENSOR_ERROR:
            #     print(f"[CODE {statusCode.VOLTAGE_SENSOR_ERROR}] Voltage Sensor Error. Data can't be readed.")

            
            if(not sum(self.sensor_alert_list) and not sum(self.temp_warning_list) and not sum(self.temp_danger_list)):
                self.send_alert_message = False
                self.sent_alert_message_time = 99999999
                self.gpio_command.turnOnOkAlert()
            else:
                self.gpio_command.turnOffOkAlert()

            self.alertMessageControl()
            # f"We have a problem with our sensors:\n Sensor number {[i+1 for i, x in enumerate(self.sensor_alert_list) if x]}"
            
            time.sleep(10)
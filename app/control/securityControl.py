import yaml
import time

from db.dbCommands import dbCommands
from security.TemperatureSystem import TemperatureSystem
from security.ExternalComunicationSystem import ExternalComunicationSystem
from utils.statusCode import statusCode
from utils.piGPIOSystem import piGPIOSystem

import logging

import RPi.GPIO as GPIO

OK = 1
WARNING = 2
DANGER = 3


class securityControl:
    def __init__(self):
        with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        self.log = logging.getLogger("root")

        self.debug = config["SERVER"]["DEBUG"]

        n_sensors = len(config['SENSORS']['TEMPERATURE_SENSOR'])

        GPIO.setmode(GPIO.BCM)
        
        ## ----------------- SECURITY CONTROL VARIABLES --------------------
        ### ARRAY USED TO ENABLE ALERT SYSTEM TO TURN ON GPIOS AND SEND MESSAGE ALERT
        self.sensor_alert_list = [0] * n_sensors
        self.temp_warning_list = [0] * n_sensors
        self.temp_danger_list = [0] * n_sensors

        ### VARIABLE TO CONTROL EXTERNAL ALERT MESSAGES
        self.ok_message = config["TELEGRAM"]["OK_MESSAGE"]
        self.sensor_problem_message = config["TELEGRAM"]["SENSOR_PROBLEM_MESSAGE"]
        self.temperature_warning_message = config["TELEGRAM"]["TEMPERATURE_WARNING_MESSAGE"]
        self.temperature_danger_message = config["TELEGRAM"]["TEMPERATURE_DANGER_MESSAGE"]
        self.send_message_time = config["TELEGRAM"]["SEND_MESSAGE_TIME_MIN"]

        self.send_alert_message = False
        self.alert_message = ""
        self.sent_alert_message_time = 9999999999
        self.problem_flag = False

        self.message_queue = []
        ## -----------------------------------------------------------------

        ### DATA BASE ACCESS CLASS ###
        self.db_command = dbCommands()

        ### TEMPERATURE SYSTEM ###
        self.tempSystem = TemperatureSystem(self.db_command)

        ### GPIO SYSTEM INIT ###
        self.gpio_command = piGPIOSystem()

        ### EXTERNAL COMUNICATION SYSTEM ###
        self.comunication = ExternalComunicationSystem()

    def alertMessageControl(self, message_queue):
        if(self.send_alert_message):
            current_time = time.time()
            elapsed_time_in_min = int((current_time - self.sent_alert_message_time)/60)

            if(elapsed_time_in_min >= self.send_message_time or elapsed_time_in_min < 0):
                while len(message_queue):
                    
                    message = message_queue.pop()
                    if(message[0] == WARNING):
                        if(self.debug):
                            self.log.info("[ALERT] - Send external WARNING alert")
                        self.comunication.warningMessage(message[1])
                    if(message[0] == DANGER):
                        if(self.debug):
                            self.log.info("[ALERT] - Send external DANGER alert")
                        self.comunication.dangerMessage(message[1])
                    if(message[0] == OK):
                        if(self.debug):
                            self.log.info("[ALERT] - Send external DANGER alert")
                        self.comunication.okMessage(message[1])
                    time.sleep(1)
                
                self.sent_alert_message_time = time.time()

    def run(self):
        while True:
            # GET LAST DATABASE TEMPERATURE ACQUIRED
            result = self.tempSystem.temperatureCheck()

            message_queue = []

            ## LOOP FOR ALL CHECKED SENSORS AND POPULATE message_queue
            for id, (sensor_name, temp, hum, status_code) in enumerate(result):
                if status_code == statusCode.OK_WAINTING:
                    if(self.debug):
                        self.log.info(f"[CODE {status_code}] {sensor_name} - Waiting for more data")
                    continue

                if status_code == statusCode.TEMPERATURE_SENSOR_ERROR:
                    self.problem_flag = True
                    self.sensor_alert_list[id] = 1
                    message_queue.append([WARNING, self.sensor_problem_message])
                    if(self.debug):
                        self.log.info(f"[CODE {status_code}] {sensor_name} - Temperature Sensor Error. Data can't be readed.")
                    continue
                else:
                    self.sensor_alert_list[id] = 0

                if status_code == statusCode.WARNING_TEMPERATURE:
                    self.problem_flag = True
                    self.temp_warning_list[id] = 1
                    message_queue.append([WARNING, self.temperature_warning_message + f"\n\nSensor: {sensor_name} \nTemperature: {temp}°C, Humidity: {hum}"])
                    if(self.debug):
                        self.log.info(f"[CODE {status_code}] {sensor_name} - WARNING! Temperature is HIGH. {temp} degrees")

                elif status_code == statusCode.DANGER_TEMPERATURE:
                    self.problem_flag = True
                    self.temp_danger_list[id] = 1
                    message_queue.append([DANGER, self.temperature_danger_message + f"\n\nSensor: {sensor_name} \nTemperature: {temp}°C, Humidity: {hum} "])
                    if(self.debug):
                        self.log.info(f"[CODE {status_code}] {sensor_name} - DANGER! Temperature is VERY HIGH. {temp} degrees")

                elif status_code == statusCode.SENSOR_OK:
                    
                    self.sensor_alert_list[id] = 0
                    self.temp_warning_list[id] = 0
                    self.temp_danger_list[id] = 0
        
                    if(self.debug):
                        self.log.info(f"[CODE {status_code}] {sensor_name} - Sensor is OK!")

            ### ------------------- TURNING OF LED STATUS AND SET TO SEND MESSAGE ALERT ----------------------
                        
            if(sum(self.sensor_alert_list)):
                self.send_alert_message = True
                self.gpio_command.turnOnTempSensorWarning()
            else:
                self.gpio_command.turnOffTempSensorWarning()

            if(sum(self.temp_warning_list)):
                self.send_alert_message = True
                self.gpio_command.turnOnTempWarning()
            else:
                self.gpio_command.turnOffTempWarning()

            if(sum(self.temp_danger_list)):
                self.send_alert_message = True
                self.gpio_command.turnOnTempDanger()
            else:
                self.gpio_command.turnOffTempDanger()

            ## TODO
            ## VOLTAGE SENSOR CHECK
            # if result == statusCode.VOLTAGE_SENSOR_ERROR:
            #     self.log.info((f"[CODE {statusCode.VOLTAGE_SENSOR_ERROR}] Voltage Sensor Error. Data can't be readed.")

            if(not sum(self.sensor_alert_list) and not sum(self.temp_warning_list) and not sum(self.temp_danger_list)):
                if self.problem_flag:
                        message_queue.append([OK, self.ok_message])
                
                self.problem_flag = False
                self.send_alert_message = False
                self.sent_alert_message_time = 99999999
                self.gpio_command.turnOnOkAlert()
            else:
                self.gpio_command.turnOffOkAlert()

            self.alertMessageControl(message_queue)
            # f"We have a problem with our sensors:\n Sensor number {[i+1 for i, x in enumerate(self.sensor_alert_list) if x]}"
            
            time.sleep(10)

            ## -----------------------------------------------------------------------------------------------
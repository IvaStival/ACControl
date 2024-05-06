import threading

from .sensorsControl import sensorControl
from .screenControl import screenControl
from .securityControl import securityControl
from .botControl import botControl
from sensors.temperature.controlDHT22 import controlDHT22

from log import log

# MAIN EXECUTION CLASS
class controlManager:
    def __init__(self):
        self.sensors_control = sensorControl()
        self.screen_control = screenControl()
        self.security_control = securityControl()
                
        self.realtime_bot = botControl()

        self.logger = log.setup_custom_log("root")
        

    def run(self):
        # INITIALIZE ALL OTHER CLASS 
        ## MANAGE ALL SENSORS
        sensor_thread = threading.Thread(target=self.sensors_control.run)
        ## MANAGE THE SCREEN
        screen_thread = threading.Thread(target=self.screen_control.run)
        ## MANAGE THE SECURITY ANALITICS AND MESSAGES
        security_thread = threading.Thread(target=self.security_control.run)
        ### REALTIME BOT SYSTEM ###
        realtime_bot_thread = threading.Thread(target=self.realtime_bot.start_poling)
                                               
        print("Starting Threads ...")

        self.logger.info("Start Sensor Thread ...")
        sensor_thread.start()
        self.logger.info("Start Screen Thread ...")
        screen_thread.start()
        self.logger.info("Start Security Thread ...")
        security_thread.start()
        self.logger.info("Start Bot Thread ...")
        realtime_bot_thread.start()


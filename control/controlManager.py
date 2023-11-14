import threading

from .sensorsControl import sensorControl
from .screenControl import screenControl
from .securityControl import securityControl
from sensors.temperature.controlDHT22 import controlDHT22

# MAIN EXECUTION CLASS
class controlManager:
    def __init__(self):
        self.sensors_control = sensorControl()
        self.screen_control = screenControl()
        self.security_control = securityControl()

    def run(self):
        # INITIALIZE ALL OTHER CLASS 
        ## MANAGE ALL SENSORS
        sensor_thread = threading.Thread(target=self.sensors_control.run)
        ## MANAGE THE SCREEN
        screen_thread = threading.Thread(target=self.screen_control.run)
        ## MANAGE THE SECURITY ANALITICS AND MESSAGES
        security_thread = threading.Thread(target=self.security_control.run)

        print("Starting Threads ...")

        sensor_thread.start()
        screen_thread.start()
        security_thread.start()

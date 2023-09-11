import yaml 
import RPi.GPIO as GPIO

## THIS CLASS WILL MANAGE ALL SIGNAL THAT WILL BE USED FOR EXTERNAL COMPONENTS
## EX: ALARM, BACKUP AC (Air Conditioning), STATUS LEDS, ... 
class piGPIOSystem:
    def __init__(self):
        GPIO.setwarnings(False)
        

        with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        
        self.gpios = (config["GPIOS"])
        self.gpios_control = {}

        for gpio in self.gpios:
            GPIO.setup(self.gpios[gpio], GPIO.OUT)
            GPIO.output(self.gpios[gpio], GPIO.LOW)
            self.gpios_control[gpio] = 0

        

    def turnOnGPIO(self, gpio_type):
        if(gpio_type not in self.gpios.keys()):
            print("GPIO Not configured. Add it to the config file")
            return False
        
        if (not self.gpios_control[gpio_type]):
            print(f"TURNING ON GPIO {self.gpios[gpio_type]}")
            GPIO.output(self.gpios[gpio_type], GPIO.HIGH)
            self.gpios_control[gpio_type] = 1
        
        return True
    
    def turnOffGPIO(self, gpio_type):
        if(gpio_type not in self.gpios.keys()):
            print("GPIO Not configured. Add it to the config file")
            return False
        
        if (self.gpios_control[gpio_type]):
            GPIO.output(self.gpios[gpio_type], GPIO.LOW)
            self.gpios_control[gpio_type] = 0
        
        return True
    
    def reset(self):
        for gpio in self.gpios:
            GPIO.output(gpio, GPIO.LOW)

    def turnOnTempSensorWarning(self):
        self.turnOnGPIO(gpio_type="TEMPERATURE_SENSOR_ALERT_PIN")

    def turnOffTempSensorWarning(self):
        self.turnOffGPIO(gpio_type="TEMPERATURE_SENSOR_ALERT_PIN")

    def turnOnTempWarning(self):
        self.turnOnGPIO(gpio_type="TEMPERATURE_WARNING_ALERT_PIN")

    def turnOffTempWarning(self):
        self.turnOffGPIO(gpio_type="TEMPERATURE_WARNING_ALERT_PIN")
        
    def turnOnTempDanger(self):
        self.turnOnGPIO(gpio_type="TEMPERATURE_DANGER_ALERT_PIN")
    
    def turnOffTempDanger(self):
        self.turnOffGPIO(gpio_type="TEMPERATURE_DANGER_ALERT_PIN")

    def turnOnVoltageAlert(self):
        self.turnOnGPIO(gpio_type="VOLTAGE_ALERT_PIN")

    def turnOffVoltageAlert(self):
        self.turnOffGPIO(gpio_type="VOLTAGE_ALERT_PIN")

    def turnOnAlarmAlert(self):
        self.turnOnGPIO(gpio_type="ALARM_ALERT_PIN")
    
    def turnOffAlarmAlert(self):
        self.turnOffGPIO(gpio_type="ALARM_ALERT_PIN")
    
    def turnOnOkAlert(self):
        self.turnOnGPIO(gpio_type="Ok_ALERT")
    
    def turnOffOkAlert(self):
        self.turnOffGPIO(gpio_type="Ok_ALERT")
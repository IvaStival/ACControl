import yaml
from utils.statusCode import statusCode

NUM_ELEMENTS=5

## TEST ONLY - REMOVE IT
UP_TEMPERATURE=0

class TemperatureSystem:
    def __init__(self, connection):
        with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        self.warning_temperature = config["TEMPERATURE_SERVER"]["WARNING_TEMP"]
        self.danger_temperature = config["TEMPERATURE_SERVER"]["DANGER_TEMP"]
        
        self.temp_history = []
        self.connection = connection
    
    def temperatureCheck(self):
        result = self.connection.getLastN(table="sensors", n=NUM_ELEMENTS).fetchall()
        temp_check_result = []

        ## WAIT FOR NUM_ELEMENT AMOUNT OF DATA ON DATABASE
        if len(result) < NUM_ELEMENTS:
            return temp_check_result.append((None, statusCode.OK_WAINTING))
        else:
            name_sensor1 = result[0][1]
            t_sensor1 = result[0][2] + UP_TEMPERATURE if result[0][2] else result[0][2] ## TEST ONLY - REMOVE IT
            h_sensor1 = result[0][3]
            name_sensor2 = result[0][4]
            t_sensor2 = result[0][5]
            h_sensor2 = result[0][6]

            ## CHECK IF THE SERSORS ARE WORKING
            if(not t_sensor1):
                temp_check_result.append([name_sensor1, 0, statusCode.TEMPERATURE_SENSOR_ERROR])
            elif(not h_sensor1):
                temp_check_result.append([name_sensor1, 0, statusCode.TEMPERATURE_SENSOR_ERROR])
            else:
                ## CHECK IF THE TEMPERATURE IS IN WARNING RANGE
                ## RETURN A WARNING STATUS CODE
                if(t_sensor1 >= self.warning_temperature and t_sensor1 < self.danger_temperature):
                    temp_check_result.append([name_sensor1, t_sensor1, statusCode.WARNING_TEMPERATURE])
                
                ## CHECK IF THE TEMPERATURE IS IN DANGER RANGE
                ## RETURN A DANGER STATUS CODE
                elif(t_sensor1 >= self.danger_temperature):
                    temp_check_result.append([name_sensor1, t_sensor1, statusCode.DANGER_TEMPERATURE])
                else:
                    temp_check_result.append([name_sensor1, t_sensor1, statusCode.SENSOR_OK])

            if(not t_sensor2):
                temp_check_result.append([name_sensor2, 0, statusCode.TEMPERATURE_SENSOR_ERROR])
                
            elif(not h_sensor2):
                temp_check_result.append([name_sensor2,0, statusCode.TEMPERATURE_SENSOR_ERROR])

            else:
                if(t_sensor2 >= self.warning_temperature and t_sensor2 < self.danger_temperature):
                    temp_check_result.append([name_sensor2, t_sensor2, statusCode.WARNING_TEMPERATURE])
                
                ## CHECK IF THE TEMPERATURE IS IN DANGER RANGE
                ## RETURN A DANGER STATUS CODE
                elif(t_sensor2 >= self.danger_temperature):
                    temp_check_result.append([name_sensor2, t_sensor2, statusCode.DANGER_TEMPERATURE])
                else:
                    temp_check_result.append([name_sensor2, t_sensor2, statusCode.SENSOR_OK])
            
            ## TODO
            ## ADD THE VOLTAGE SENSOR CHECK

            return temp_check_result

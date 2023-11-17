import yaml
from utils.statusCode import statusCode

NUM_ELEMENTS=3
SENSOR_OFF = 1
WARNING = 2
DANGER = 3

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

    ## THIS FUNCTION is USED TP CHECK NUM_ELEMENT TEMPERATURE BEFORE SEND A STATUS WARNING/DANGER ALERT
    def _temperatureStatus(self, temperatures):
        sensor1_status = 0
        sensor2_status = 0
        warning_counter_s1 = 0
        danger_counter_s1 = 0
        warning_counter_s2 = 0
        danger_counter_s2 = 0

        for readed_temp in temperatures:
            t_sensor1 = readed_temp[2] 
            h_sensor1 = readed_temp[3]
            t_sensor2 = readed_temp[5]
            h_sensor2 = readed_temp[6]

            ## CHECK IF THERE IS A SENSOR DATA
            if(not t_sensor1 or not h_sensor1):
                sensor1_status = SENSOR_OFF
            else:
                ## CHECK IF THE TEMPERATURE IS BETWEEN WARINIG AND DANGE TEMPERATURE IF SO PLUS ONE TO THE COUNTER WARNING
                if(t_sensor1 >= self.warning_temperature and t_sensor1 < self.danger_temperature):
                    warning_counter_s1 += 1
                ## ELSE ADD 1 TO DANGER COUNTER
                elif(t_sensor1 >= self.danger_temperature):
                    danger_counter_s1 += 1

            if(not t_sensor2 or not h_sensor2):
                sensor2_status = SENSOR_OFF
            else:
                ## HERE IS THE SAME BUT TO SENSOR 2
                if(t_sensor2 >= self.warning_temperature and t_sensor2 < self.danger_temperature):
                    warning_counter_s2 += 1
                elif(t_sensor2 >= self.danger_temperature):
                    danger_counter_s2 += 1
        
        ## COUNTER CHECK
        # IN THIS PART WE WILL CHECK OUR COUNTERS
        # IF THE COUNTER IS EQUAL TO "NUM_ELEMENTS" WE WILL RETURN ONE OF THREE POSSIBILITIES FOR EACH SENSOR
        # SENSOR_OFF (1)
        # WARNING (2)
        # DANGER (3)

        # IF THERE ARE TWO WARNING AND ONE DANGER WE WILL RAISE A WARNING STATUS
        # A DANGER WILL BE RAISED ONLY IF WE HAVE A "NUM_ELEMENTS" COUNT
        if warning_counter_s1 + danger_counter_s1 == NUM_ELEMENTS and danger_counter_s1 < NUM_ELEMENTS:
            sensor1_status = WARNING
        elif danger_counter_s1 == NUM_ELEMENTS:
            sensor1_status = DANGER
        
        if warning_counter_s2 + danger_counter_s2 == NUM_ELEMENTS and danger_counter_s2 < NUM_ELEMENTS:
            sensor2_status = WARNING
        elif danger_counter_s2 == NUM_ELEMENTS:
            sensor2_status = DANGER

        ## HERE WE WILL RETURN THE LAST DATA INFORMATION THAT WE HAVE WITH THE STATUS
        s1_name = temperatures[-1][1]
        t1 = temperatures[-1][2]
        h1 = temperatures[-1][3]
        s2_name = temperatures[-1][4]
        t2 = temperatures[-1][5]
        h2 = temperatures[-1][6]

        return [(s1_name, t1, h1, sensor1_status), (s2_name, t2, h2, sensor2_status)]
    
    def temperatureCheck(self):
        temperature_data = self.connection.getLastN(table="sensors", n=NUM_ELEMENTS).fetchall()
        temp_check_result = []

        ## WAIT FOR NUM_ELEMENT AMOUNT OF DATA ON DATABASE
        if len(temperature_data) < NUM_ELEMENTS:
            return temp_check_result.append((None, statusCode.OK_WAINTING))
        else:
            # name_sensor1 = result[0][1]
            # t_sensor1 = result[0][2] + UP_TEMPERATURE if result[0][2] else result[0][2] ## TEST ONLY - REMOVE IT
            # h_sensor1 = result[0][3]
            # name_sensor2 = result[0][4]
            # t_sensor2 = result[0][5]
            # h_sensor2 = result[0][6]

            # ## CHECK IF THE SERSORS ARE WORKING
            # if(not t_sensor1):
            #     temp_check_result.append([name_sensor1, 0, statusCode.TEMPERATURE_SENSOR_ERROR])
            # elif(not h_sensor1):
            #     temp_check_result.append([name_sensor1, 0, statusCode.TEMPERATURE_SENSOR_ERROR])
            # else:
            #     ## CHECK IF THE TEMPERATURE IS IN WARNING RANGE
            #     ## RETURN A WARNING STATUS CODE
            #     if(t_sensor1 >= self.warning_temperature and t_sensor1 < self.danger_temperature):
            #         temp_check_result.append([name_sensor1, t_sensor1, statusCode.WARNING_TEMPERATURE])
                
            #     ## CHECK IF THE TEMPERATURE IS IN DANGER RANGE
            #     ## RETURN A DANGER STATUS CODE
            #     elif(t_sensor1 >= self.danger_temperature):
            #         temp_check_result.append([name_sensor1, t_sensor1, statusCode.DANGER_TEMPERATURE])
            #     else:
            #         temp_check_result.append([name_sensor1, t_sensor1, statusCode.SENSOR_OK])

            # if(not t_sensor2):
            #     temp_check_result.append([name_sensor2, 0, statusCode.TEMPERATURE_SENSOR_ERROR])
                
            # elif(not h_sensor2):
            #     temp_check_result.append([name_sensor2,0, statusCode.TEMPERATURE_SENSOR_ERROR])

            # else:
            #     if(t_sensor2 >= self.warning_temperature and t_sensor2 < self.danger_temperature):
            #         temp_check_result.append([name_sensor2, t_sensor2, statusCode.WARNING_TEMPERATURE])
                
            #     ## CHECK IF THE TEMPERATURE IS IN DANGER RANGE
            #     ## RETURN A DANGER STATUS CODE
            #     elif(t_sensor2 >= self.danger_temperature):
            #         temp_check_result.append([name_sensor2, t_sensor2, statusCode.DANGER_TEMPERATURE])
            #     else:
            #         temp_check_result.append([name_sensor2, t_sensor2, statusCode.SENSOR_OK])
            
            # ## TODO
            ## ADD THE VOLTAGE SENSOR CHECK            
            result = self._temperatureStatus(temperature_data)

            s1_name = result[0][0]
            t1 = result[0][1]
            h1 = result[0][2]
            s1_status = result[0][3]
            s2_name = result[1][0]
            t2 = result[1][1]
            h2 = result[1][2]       
            s2_status = result[1][3]     
            ## CHECK IF THE SERSORS ARE WORKING
        
            if s1_status == SENSOR_OFF:
                temp_check_result.append([s1_name, 0, 0, statusCode.TEMPERATURE_SENSOR_ERROR])
            else:
                ## CHECK IF THE TEMPERATURE IS IN WARNING RANGE
                ## RETURN A WARNING STATUS CODE
                if s1_status == WARNING:
                    temp_check_result.append([s1_name, t1, h1, statusCode.WARNING_TEMPERATURE])
                
                ## CHECK IF THE TEMPERATURE IS IN DANGER RANGE
                ## RETURN A DANGER STATUS CODE
                elif s1_status == DANGER:
                    temp_check_result.append([s1_name, t1, h1, statusCode.DANGER_TEMPERATURE])
                else:
                    temp_check_result.append([s1_name, t1, h1, statusCode.SENSOR_OK])

            if s2_status == SENSOR_OFF:
                temp_check_result.append([s2_name, 0, 0, statusCode.TEMPERATURE_SENSOR_ERROR])

            else:
                if s2_status == WARNING:
                    temp_check_result.append([s2_name, t2, h2, statusCode.WARNING_TEMPERATURE])
                
                ## CHECK IF THE TEMPERATURE IS IN DANGER RANGE
                ## RETURN A DANGER STATUS CODE
                elif s2_status == DANGER:
                    temp_check_result.append([s2_name, t2, h2, statusCode.DANGER_TEMPERATURE])
                else:
                    temp_check_result.append([s2_name, t2, h2, statusCode.SENSOR_OK])
            
            ## TODO

            return temp_check_result

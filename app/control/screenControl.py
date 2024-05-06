import yaml
import time
from lcd.controlLCD import controlLCD
from db.dbCommands import dbCommands

class screenControl:
    def __init__(self):
        with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        #### LCD CONFIG DATA ####
        address = config["LCD"]["ADDRESS"]
        port = config["LCD"]["PORT"]
        charmap = config["LCD"]["CHARMAP"]
        cols = config["LCD"]["COLS"]
        rows = config["LCD"]["ROWS"]
        i2c_expander = config["LCD"]["I2C_EXPANDER"]

        

        #INITIALIZE LCD CONTROL
        self.lcd_control = controlLCD(address, port, charmap, cols, rows, i2c_expander)

        # #### DB CONFIG DATA ####
        # self.user = config["DB"]["USER"]
        # self.password = config["DB"]["PASSWORD"]
        # self.host = config["DB"]["HOST"]
        # self.port = config["DB"]["PORT"]
        # self.db_name = config["DB"]["DBNAME"]

        # self.db_command = dbCommands(self.user, self.password, self.host, self.port, self.db_name)
        self.db_command = dbCommands()

    def run(self):
        while True:
            result = self.db_command.getLast(table='sensors')
            
            for (id, s1, t1, h1, s2, t2, h2, create_at) in result:
                self.lcd_control.write([f"T1:{t1}", f"T2:{t2}"], [f"H1:{h1}", f"H2:{h2}"]),

            time.sleep(2)
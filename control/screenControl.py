import yaml
from lcd.controlLCD import controlLCD
from db.dbCommands import dbCommands

class screenControl:
    def __init__(self):
        with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        #### LCD CONFIG DATA ####
        pin_rs = config["LCD"]["PIN_RS"]
        pin_e = config["LCD"]["PIN_E"]
        pins_data = config["LCD"]["PINS_DATA"]

        #INITIALIZE LCD CONTROL
        self.lcd_control = controlLCD(pin_rs, pin_e, pins_data)

        #### DB CONFIG DATA ####
        self.user = config["DB"]["USER"]
        self.password = config["DB"]["PASSWORD"]
        self.host = config["DB"]["HOST"]
        self.port = config["DB"]["PORT"]
        self.db_name = config["DB"]["DBNAME"]

        self.db_command = dbCommands(self.user, self.password, self.host, self.port, self.db_name)

    def run(self):
        result = self.db_command.getLast(table='sensors')
        for (id, t1, h1, t2, h2, create_at) in result:
            self.lcd_control.write([f"T1:{t1}", f"T2:{t2}"], [f"H1:{h1}", f"H2:{h2}"]),
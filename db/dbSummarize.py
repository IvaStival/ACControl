import yaml
from db.dbCommands import dbCommands

class dbSummarize:
    def __init__(self):
        with open("./config/config.yaml", 'r') as file:
            config = yaml.safe_load(file)
        
        self.db_command = dbCommands()
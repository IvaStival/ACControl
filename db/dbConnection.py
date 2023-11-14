import yaml
import mariadb
import sys

class dbConnection:
    def __init__(self):
        with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        #### DB CONFIG DATA ####
        self.user = config["DB"]["USER"]
        self.password = config["DB"]["PASSWORD"]
        self.host = config["DB"]["HOST"]
        self.port = config["DB"]["PORT"]
        self.db_name = config["DB"]["DBNAME"]

    def connect(self):
        
        try:
            self.conn = mariadb.connect(user=self.user, 
                                        password=self.password, 
                                        host=self.host, 
                                        port=self.port, 
                                        database=self.db_name)
    
            self.conn.autocommit = True
            self.cur = self.conn.cursor()

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Plataform: {e}")
            sys.exit(1)

        else:
            print("Connection estabilished.")
    

    def query(self, query_command, data=None):
        try:
            self.cur.execute(query_command, data)
            # self.conn.commit()
            return self.cur
        except mariadb.Error as e:
            print(f"Error to execute query: {e}")

    def close(self):
        self.cur.close()
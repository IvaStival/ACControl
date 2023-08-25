import mariadb
import sys

class dbConnection:
    def __init__(self, user, password, host, port, database):

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def connect(self):
        
        try:
            self.conn = mariadb.connect(user=self.user, 
                                        password=self.password, 
                                        host=self.host, 
                                        port=self.port, 
                                        database=self.database)
    
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
from .dbConnection import dbConnection

class dbCommands:
    
    def __init__(self, user, password, host, port, database):
        
        self.connection = dbConnection(user, password, host, port, database)
        self.connection.connect()
        

    def createTable(self):
        command = """CREATE TABLE IF NOT EXISTS sensors (id INT AUTO_INCREMENT PRIMARY KEY, 
                                            t1 FLOAT, 
                                            h1 FLOAT, 
                                            t2 FLOAT, 
                                            h2 FLOAT,
                                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                                            )"""
        
        result = self.connection.query(command)
        
    def deleteTable(self):
        command = "DROP TABLE accontrol"
        self.connection.query(command)

    def insert(self, t1=None, h1=None, t2=None, h2=None):
        command = f"INSERT INTO sensors (t1, h1, t2, h2) VALUES (%s, %s, %s, %s)"
        self.connection.query(command, (t1, h1, t2, h2))

    def getAll(self, table):
        command = f"SELECT * FROM {table}"
        return self.connection.query(command)
    
    def getById(self, table, id):
        pass

    def getLast(self, table):
        command = f"SELECT * FROM {table} ORDER BY created_at DESC LIMIT 1;"
        return self.connection.query(command)

    def getLastN(self, table, n):
        pass

    def getByMonth(self, table, month):
        pass

    def getByYear(self, table, yeay):
        pass


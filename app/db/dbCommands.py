from .dbConnection import dbConnection

class dbCommands:
    
    def __init__(self):
        
        self.connection = dbConnection()
        self.connection.connect()
        

    def createTable(self):
        command = """CREATE TABLE IF NOT EXISTS sensors (id INT AUTO_INCREMENT PRIMARY KEY, 
                                            s1 VARCHAR(100),
                                            t1 FLOAT, 
                                            h1 FLOAT, 
                                            s2 VARCHAR(100),
                                            t2 FLOAT, 
                                            h2 FLOAT,
                                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                                            )"""
        
        result = self.connection.query(command)

    def createSummarizeTable(self):
        command = """CREATE TABLE IF NOT EXISTS summarize_sensor (id INT AUTO_INCREMENT PRIMARY KEY, 
                                            year VARCHAR(10),
                                            month VARCHAR(10),
                                            day VARCHAR(10),
                                            s1 VARCHAR(100),
                                            t1 FLOAT, 
                                            h1 FLOAT, 
                                            s2 VARCHAR(100),
                                            t2 FLOAT, 
                                            h2 FLOAT,
                                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                                            )"""
        

        # CREATE TABLE IF NOT EXISTS summarize_sensor (id INT AUTO_INCREMENT PRIMARY KEY, year VARCHAR(10),month VARCHAR(10),day VARCHAR(10),s1 VARCHAR(100),t1 FLOAT, h1 FLOAT, s2 VARCHAR(100),t2 FLOAT, h2 FLOAT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        result = self.connection.query(command)
        
    def deleteTable(self):
        command = "DROP TABLE accontrol"
        self.connection.query(command)

    def insert(self, s1=None, t1=None, h1=None, s2=None, t2=None, h2=None, table="sensors"):
        command = f"INSERT INTO {table} (s1, t1, h1, s2, t2, h2) VALUES (%s, %s, %s, %s, %s, %s)"
        self.connection.query(command, (s1, t1, h1, s2, t2, h2))

    # IN THIS INSERT WE'LL RECEIVE A STRUCTURE LIKE THIS:
    # {'s1': '<sensor_name>', t1: 30, h1: 70, s2: '<sensor_name>', ...}
    def insert(self, data):
        keys = tuple(data.keys())
        variable_names = ', '.join(keys)
        n_percent_s = '%s,' *  len(data)
        values = tuple(data.values())

        command = f"INSERT INTO sensors ({variable_names}) VALUES ({n_percent_s[:-1]})"
        self.connection.query(command, values)


    def getAll(self, table):
        command = f"SELECT * FROM {table}"
        return self.connection.query(command)
    
    def getById(self, table, id):
        pass

    def getLast(self, table):
        command = f"SELECT * FROM {table} ORDER BY created_at DESC LIMIT 1;"
        return self.connection.query(command)

    def getLastN(self, table, n):
        command = f"SELECT * FROM {table} ORDER BY created_at DESC LIMIT {n};"
        return self.connection.query(command)

    def summarizeData(self, period, today, month):
    
        select_command = """SELECT  EXTRACT(year FROM created_at) as year, 
                            EXTRACT(month FROM created_at) as month, 
                            EXTRACT({period} FROM created_at) as {period}, 
                            s1,
                            avg(t1) as t1_avg,
                            avg(h1) as h1_avg,
                            s2,
                            avg(t2) as t2_avg,
                            avg(h2) as h2_avg
                            from sensors where EXTRACT({period} FROM created_at) != {today} OR EXTRACT(month FROM created_at) != {month}
                            GROUP BY EXTRACT({period} FROM created_at)"""
        
        # summarized_data = self.connection.query(command)

        # command = f"INSERT INTO summarize_sensor (year, month, day, s1, t1, h1, s2, t2, h2) SELECT EXTRACT(year FROM created_at) as year, EXTRACT(month FROM created_at) as month, EXTRACT({period} FROM created_at) as {period}, s1,avg(t1) as t1_avg,avg(h1) as h1_avg,s2,avg(t2) as t2_avg,avg(h2) as h2_avg from sensors where EXTRACT({period}} FROM created_at) != {today} OR EXTRACT(month FROM created_at) != {month} GROUP BY EXTRACT({period} FROM created_at)"
        command = f"INSERT INTO summarize_sensor (year, month, day, s1, t1, h1, s2, t2, h2) {select_command}"
        self.connection.query(command)

    def _deleteSummarizedData(self, period, today, month):

        command = f"DELETE FROM sensors WHERE id IN (SELECT id from sensors where EXTRACT({today} FROM created_at) != 14 OR EXTRACT(month FROM created_at) != 11)"
        self.connection.query(command)
        
    def getByYear(self, table, yeay):
        pass
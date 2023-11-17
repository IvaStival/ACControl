import yaml
from db.dbCommands import dbCommands

class dbSummarize:
    def __init__(self):
        with open("./config/config.yaml", 'r') as file:
            config = yaml.safe_load(file)

        summarize_time = config["DATA"]["SUMMIRIZE_TIME"]


        # elif(summarize_time == "WE")
        # select s1, avg(t1) as sm_t1, avg(h1) as sm_h1, s2, avg(t2) as sm_t2, avg(h2) as sm_h2 from (select * from sensors order by id asc LIMIT 10) as subquery;
        
        # select EXTRACT(day FROM created_at) as day, avg(t1) as t1_mean from (select * from sensors order by id asc LIMIT 1000) as subquery GROUP BY EXTRACT(day FROM created_at);

        # SELECT EXTRACT(year FROM created_at) as YEAR, 
        # SUM(t1) as sum_t1 FROM sensors 
        # GROUP BY EXTRACT(year FROM created_at);
        self.db_command = dbCommands()




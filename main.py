from control.controlManager import controlManager

import time

if __name__ == "__main__":
    manager = controlManager()
    manager.run()
    # # user, password, host, port, database
    # db_command = dbCommands("rv", "narsil", "localhost", 3306, "accontrol")
    # # db_command.createTable()
    # db_command.insert(t1=20.0, h1=95.0, t2=23.0, h2=96.0)
    # time.sleep(1)
    # result = db_command.get_all(table="sensors")
    # for t1 in result:
    #     print(t1)
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_custom_log(name):
    now = datetime.now()
    formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s")

    # handler = logging.StreamHandler()
    # handler.setFormatter(formatter)
    
    # logging.basicConfig(filename=f"log/log_files/LogFile_{now.strftime('%d-%m-%y')}",filemode="a",format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",datefmt='%H:%M:%S')
    handler = TimedRotatingFileHandler(filename=f"log/log_files/LogFile.log", when='midnight', interval=1, backupCount=7)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.SESSION_TIME_TO_LIVE = 60 * 5
    
    # logger.addHandler(handler)

    return logger
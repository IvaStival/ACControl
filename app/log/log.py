import yaml
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_custom_log(name):
    with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
    
    logLevel = config["LOG"]["LEVEL"]

    now = datetime.now()
    formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s")

    # logging.basicConfig(filename=f"log/log_files/LogFile_{now.strftime('%d-%m-%y')}",filemode="a",format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",datefmt='%H:%M:%S')
    handler = TimedRotatingFileHandler(filename=f"log/log_files/LogFile.log", when='midnight', interval=1, backupCount=7)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logLevel)
    logger.addHandler(handler)
    logger.SESSION_TIME_TO_LIVE = 60 * 5
    
    # logger.addHandler(handler)

    return logger
import telebot
import yaml
import time
import logging

from db.dbCommands import dbCommands

class botControl:
    def __init__(self):
        self.started = False
        self.log = logging.getLogger("root")
        with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)

            token = config["TELEGRAM"]["TOKEN_SENDER"]
            self.chat_id = config["TELEGRAM"]["CHATGROUPID"]
            self.bot = telebot.TeleBot(token)
            self.bot.SESSION_TIME_TO_LIVE = 5 * 60

            self.db_command = dbCommands()

            @self.bot.message_handler(commands=["start", "hello"])
            def send_welcome(message):
                self.bot.reply_to(message, "Hi, how are you going?")

            @self.bot.message_handler(commands=["status"])
            def send_status(message):
                result = self.db_command.getLast(table='sensors')
                self.log.info("Info Requested")
                for (id, s1, t1, h1, s2, t2, h2, create_at) in result:
                    self.bot.reply_to(message, f"Temperature\n🌡️{s1} - {t1}°C\n🌡️{s2} - {t2}°C\n\nHumidity\n💧{s1} - {h1}\n💧{s2} - {h2}")

    def check_connection(self):
        if not self.bot.get_me():
            self.log.info("Bot disconnected. Attempting to reconnect...")
            self.bot.polling()
            self.log.info("Reconnected successfully.")
        elif not self.started:
            
            self.log.info("Connecting Bot...")
            self.bot.polling()
            self.started = True
            self.log.info("Bot Connected...")

    def start_poling(self):
        while True:
            try:
                self.check_connection()
                time.sleep(60) # Chech each 1min
            except:
                self.log.info("Error on starting bot")
        
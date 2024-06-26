import yaml
import telebot
import logging

class ExternalComunicationSystem:
    def __init__(self):
        with open('./config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        token = config["TELEGRAM"]["TOKEN"]
        self.chat_id = config["TELEGRAM"]["CHATGROUPID"]
        self.bot = telebot.TeleBot(token)

        self.danger_temp = config["TEMPERATURE_SERVER"]["DANGER_TEMP"]
        self.warning_temp = config["TEMPERATURE_SERVER"]["WARNING_TEMP"]

        self.log = logging.getLogger("root")
    
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.reply_to(message, f"{self.bot.get_me()}")

        # @self.bot.message_handler(func=lambda msg:True)
        # def echo_all(message):
        #     self.bot.reply_to(message, message.text)

        # self.bot.infinity_polling()

    def sendMessage(self, message):
        self.bot.send_message(self.chat_id, message)

    def okMessage(self, message):
        self.log.info(f"Sending [OK] message - {message}")
        self.sendMessage(f"✅ [OK] - {message}")

    def warningMessage(self, message):
        self.log.info(f"Sending [WARNING] message - {message}")
        self.sendMessage(f"⚠️ [WARNING] - {message}")

    def dangerMessage(self, message):
        self.log.info(f"Sending [DANGER] message - {message}")
        self.sendMessage(f"‼️🔥🚒 [DANGER] - {message}")
import telebot
from core.agent import Agent

class Bot():
    def __init__(self, token, agent=None):
        self.token = token
        self.bot = telebot.TeleBot(token=self.token)
        
        self.target = None
        self.model = agent if agent is not None else Agent()
        print("<< Bot initialized >> ")

        self.sessions = []

    

    def start(self):
        @self.bot.message_handler(func=lambda m: not m.text.startswith("/"))
        def handle_message(message):
            chat_id = message.chat.id
            if chat_id not in self.sessions:
                self.sessions[chat_id] = {"history": []}

            history = self.sessions[chat_id]["history"]
            history.append({"role": "user", "content": message.text})

            def send_response(response):
                if not response:
                    response = "Sem resposta."

                history.append({"role": "assistant", "content": response})
                self.bot.send_message(message.chat.id, response)
            
            self.model.query(history, send_response)


        self.bot.polling()



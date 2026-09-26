import os
from dotenv import load_dotenv

class config:
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv("TOKEN")
        self.APIKEY = os.getenv("OPENAI_API_KEY")

cfg = config()
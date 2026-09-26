import os
from dotenv import load_dotenv

class config:
    def __init__(self):
        load_dotenv()
        self.LLM_PROVIDER = os.getenv("LLM_PROVIDER")
        self.LLM_API_KEY = os.getenv("LLM_API_KEY")
        self.LLM_INTEGRATION_TOKEN = os.getenv("LLM_INTEGRATION_TOKEN")
        self.LLM_MODEL = os.getenv("LLM_MODEL")
        self.LLM_BASE_URL = os.getenv("LLM_BASE_URL")

cfg = config()
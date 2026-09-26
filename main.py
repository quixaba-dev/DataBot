from bot.discord import Bot
from core.agent import Agent
from config import cfg
from providers.openaicompatible import OpenAICompatible

provider = OpenAICompatible()

Agent_instance = Agent(provider=provider)

if __name__ == '__main__':
    bot = Bot(cfg.LLM_INTEGRATION_TOKEN, agent=Agent_instance)
    bot.start()
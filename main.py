from core.bot import Bot
from core.agent import Agent
from config import cfg

Agent_instance = Agent(api_key=cfg.APIKEY)

if __name__ == '__main__':
    bot = Bot(cfg.TOKEN, agent=Agent_instance)
    bot.start()
    bot.bot.run(cfg.TOKEN)
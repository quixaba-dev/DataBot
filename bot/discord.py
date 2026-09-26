from core.agent import Agent
import asyncio
from discord.ext import commands


class NexusBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=".",
            self_bot=True
        )

class Bot():
    def __init__(self, token, agent=None):
        self.token = token
        self.bot = NexusBot()
        
        self.target = None
        self.model = agent if agent is not None else Agent()
        print("<< Bot initialized >> ")
    
    def start(self):
        @self.bot.command("transcend")
        async def handle(ctx, *, prompt):
            response = await self.model.query(prompt)
            content = response["response"]

            limit = 2000
            for i in range(0, len(content), limit):
                await ctx.send(content[i:i+limit])

        self.bot.run(self.token)
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

            async def send_response(ctx, response: str):
                header = "### 🧠 DataCenter AI\n\n"
                continuation = "-# DataCenter AI · continuação\n\n"

                first_limit = 2000 - len(header)

                await ctx.send(header + response[:first_limit])

                remaining = response[first_limit:]

                while remaining:
                    limit = 2000 - len(continuation)

                    await ctx.send(
                        continuation + remaining[:limit]
                    )

                    remaining = remaining[limit:]

            response = await self.model.query(prompt)
            content = response["response"]

            await send_response(ctx, content)

        self.bot.run(self.token)
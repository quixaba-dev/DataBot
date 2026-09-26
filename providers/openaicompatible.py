from .base import BaseProvider, ToolCall, ProviderResponse
from openai import AsyncOpenAI
from config import cfg
import json

class OpenAICompatible(BaseProvider):
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=cfg.LLM_API_KEY,
            base_url=cfg.LLM_BASE_URL
        )

    async def generate(self, messages, tools=None):
        kwargs = {
            "model": cfg.LLM_MODEL,
            "messages": messages,
            "temperature": 0.1,
            "tools": tools,
            "tool_choice": "auto"
        }

        response = await self.client.chat.completions.create(**kwargs)
        message = response.choices[0].message

        tool_calls = [
            ToolCall(
                name=tool.function.name,
                arguments=json.loads(tool.function.arguments)
            )
            for tool in (message.tool_calls or [])
        ]

        return ProviderResponse(
            content=message.content,
            tool_calls=tool_calls
        )
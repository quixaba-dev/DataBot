from openai import OpenAI
from core.rag import RAG
from tools.ToolCaller import ToolCaller
import json
import asyncio



class Agent:
    def __init__(self, api_key, model="openai/gpt-oss-120b"):
        try:
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            self.model = model
            print("Initialized.")
        except Exception as e:
            return print(e)

        self.ToolCaller = ToolCaller()

        with open("bot/rules.txt", encoding="utf-8") as f:
            for linha in f:
                self.rules = "\n".join(linha)
    
    async def query(self, query, callback):
        messages = [
            {"role": "assistant", "content": self.rules},
        ]
        contexto = "\n\n".join(RAG.search(query, k=10))

        messages.append({
            "role": "user",
            "content": f"""
Contexto:

{contexto}

query:

{query}
"""
        })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            tools=self.ToolCaller.tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        result = None

        if message.tool_calls:
            tool = message.tool_calls[0]
            args = json.loads(tool.function.arguments)

            result = self.ToolCaller.call_tool(
                tool.function.name, callback,
                **args
            )
        else:
            result = message.content

        await callback(result)

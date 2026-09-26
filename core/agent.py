from openai import AsyncOpenAI
from core.rag import RAG
from tools.ToolCaller import ToolCaller
import json
import logging

logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, api_key, model="openai/gpt-oss-120b"):
        try:
            self.client = AsyncOpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            self.model = model
            print("Initialized.")

        except Exception as e:
            print(e)
            return

        self.ToolCaller = ToolCaller()
        

        with open("bot/rules.txt", encoding="utf-8") as f:
            self.rules = f.read()

    async def query(self, query, callback):
        messages = [
            {
                "role": "system",
                "content": self.rules
            }
        ]

        resultados = RAG.search(query, k=15)

        contexto = "\n\n".join(resultados)

        if not contexto:
            logger.warning("No context found - Verify RAG & Data Folder")

        logger.info(f"Documentos recuperados: {len(resultados)}")
        logger.info(f"Caracteres do contexto: {len(contexto):,}")

        messages.append({
            "role": "user",
            "content": f"""
<RAG_CONTEXT>
{contexto}
</RAG_CONTEXT>

<USER_QUERY>
{query}
</USER_QUERY>
"""
        })

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            tools=self.ToolCaller.tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:
            tool = message.tool_calls[0]
            args = json.loads(tool.function.arguments)

            result = await self.ToolCaller.call_tool(
                tool.function.name,
                callback,
                **args
            )
        else:
            result = message.content

        debug_result = {
            "response": result,
            "context": contexto,
            "documents": resultados,
            "document_count": len(resultados),
            "context_characters": len(contexto)
        }

        await callback(debug_result["response"])

        return debug_result
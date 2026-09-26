from core.rag import RAG
from tools.ToolCaller import ToolCaller
import logging

logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, provider):

        self.provider = provider
        self.ToolCaller = ToolCaller()
        
        with open("bot/rules.txt", encoding="utf-8") as f:
            self.rules = f.read()

    async def query(self, query):
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

        """"

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            tools=self.ToolCaller.tools,
            tool_choice="auto"
        )

        """

        response = await self.provider.generate(messages, self.ToolCaller.tools)

        if response.tool_calls:
            tool = response.tool_calls[0]
            result = await self.ToolCaller.call_tool(
                tool.name,
                **tool.arguments
            )
        else:
            result = response.content

        debug_result = {
            "response": result,
            "context": contexto,
            "documents": resultados,
            "document_count": len(resultados),
            "context_characters": len(contexto)
        }

        return debug_result
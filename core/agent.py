from core.rag import RAG
from tools.ToolCaller import ToolCaller
import logging

logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, provider):

        self.rag = RAG()
        self.provider = provider
        self.ToolCaller = ToolCaller()
        
        with open("bot/rules.txt", encoding="utf-8") as f:
            self.rules = f.read()

        self.messages = [
            {
                "role": "system",
                "content": self.rules
            }
        ]

    async def query(self, query):
        if self.rag.available:
            results = self.rag.search(
                query,
                k=15
            )
        else:
            results = [
                """
        No external knowledge base is currently available.

        Answer using your own knowledge and the available tools.
        Do not claim or imply that information was retrieved from the local
        knowledge base. Use the available tools when they are appropriate
        for obtaining additional information.
        """.strip()
            ]

        contexto = "\n\n".join(results)

        if not contexto:
            logger.warning("No context found - Verify RAG & Data Folder")

        logger.info(f"Documentos recuperados: {len(results)}")
        logger.info(f"Caracteres do contexto: {len(contexto):,}")

        self.messages.append({
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

        response = await self.provider.generate(self.messages, self.ToolCaller.tools)

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
            "documents": results,
            "document_count": len(results),
            "context_characters": len(contexto)
        }

        return debug_result
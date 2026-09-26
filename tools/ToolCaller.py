import threading
from tools.tools import Tools

tools=[
    {
        "type": "function",
        "function": {
            "name": "sherlock",
            "description": "Pesquisa um usuário utilizando Sherlock.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Nome do usuário."
                    }
                },
                "required": ["username"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Pesquisa informações na internet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Termo ou consulta a ser pesquisada."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "holehe",
            "description": "Pesquisa um email utilizando Holehe.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Endereço de email."
                    }
                },
                "required": ["email"]
            }
        }
    }
]


class ToolCaller:
    def __init__(self, tools=tools):
        self.tools = tools
        print("<< ToolCaller initialized >>")

    async def call_tool(self, tool_name, **kwargs):
        registered = any(
            tool["type"] == "function"
            and tool["function"]["name"] == tool_name
            for tool in self.tools
        )

        if not registered:
            return f"Tool '{tool_name}' não encontrada."

        function = getattr(Tools, tool_name, None)

        if function is None:
            return f"Tool '{tool_name}' não implementada."

        return await function(**kwargs)
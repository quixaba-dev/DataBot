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
        # Inicialização simples do ToolCaller, armazenando a lista de ferramentas fornecida.
    
    async def call_tool(self, tool_name, callback, **kwargs):
        for tool in self.tools:

            if (
                tool["type"] == "function"
                and tool["function"]["name"] == tool_name
            ):

                if tool_name == "sherlock":
                    username = kwargs.get("username")

                    if not username:
                        return "Erro: 'username' não fornecido."

                    await Tools.sherlock(username, callback)

                    return f"Pesquisa finalizada para o usuário: {username}"


                if tool_name == "holehe":
                    email = kwargs.get("email")

                    if not email:
                        return "Erro: 'email' não fornecido."

                    await Tools.holehe(email, callback)

                    return f"Pesquisa finalizada para o email: {email}"

        return f"Tool '{tool_name}' não encontrada."



        return f"Erro: Ferramenta '{tool_name}' não encontrada." # Retorno com erro caso tool_name não seja encontrado
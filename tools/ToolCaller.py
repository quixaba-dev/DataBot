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
    
    def call_tool(self, tool_name, callback, **kwargs):
        for tool in self.tools: # Percorre a lista de tools

            if tool["type"] == "function" and tool["function"]["name"] == tool_name: #Se a tool for function e o nome da função for igual ao tool_name

                if tool_name == "sherlock": # Se tool_name for search_user
                    username = kwargs.get("username") # Pega o valor de username através dos kwargs
                    if username:
                        threading.Thread(target=Tools.sherlock, args=(username, callback)).start()
                        return f"Pesquisa iniciada para o usuário: {username}"
                    else: 
                        return "Erro: 'username' não fornecido." # Retorno com erro caso username não seja fornecido



                if tool_name == "holehe": # Se tool_name for search_email
                    email = kwargs.get("email") # Pega o valor de email através dos kwargs
                    if email:
                        threading.Thread(target=Tools.holehe, args=(email, callback)).start() # Chama search_email com threading
                        return f"Pesquisa iniciada para o email: {email}"
                    else:
                        return "Erro: 'email' não fornecido." # Retorno com erro caso email não seja fornecido



        return f"Erro: Ferramenta '{tool_name}' não encontrada." # Retorno com erro caso tool_name não seja encontrado
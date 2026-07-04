import subprocess
from googlesearch import search

class Tools:
    @staticmethod
    def sherlock(username, callback):
            try:
                resultado = subprocess.run(
                    ["sherlock", username],
                    capture_output=True,
                    text=True,
                    encoding="utf-8"
                )
                print(resultado.stdout if resultado.returncode == 0 else resultado.stderr)
                output = resultado.stdout if resultado.returncode == 0 else resultado.stderr
                callback(output)  # Chama o callback com a saída do comando

            except Exception as e:
                print(f"Exceção ao executar sherlock para {username}: {e}")


    @staticmethod
    def holehe(email, callback):
            try:
                resultado = subprocess.run(
                    ["holehe", email],
                    capture_output=True,
                    text=True,
                    encoding="utf-8"
                )
                print(resultado.stdout if resultado.returncode == 0 else resultado.stderr)
                output = resultado.stdout if resultado.returncode == 0 else resultado.stderr
                callback(output)  # Chama o callback com a saída do comando

            except Exception as e:
                print(f"Exceção ao executar holehe para {email}: {e}")
    




    @staticmethod
    def search(query, callback):
        try:
            results = []
            for j in search(query, num_results=10):
                results.append(j)
            callback("\n".join(results))  # Chama o callback com os resultados da pesquisa
        except Exception as e:
            print(f"Exceção ao executar pesquisa para {query}: {e}")
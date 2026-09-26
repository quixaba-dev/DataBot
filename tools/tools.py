import asyncio
from googlesearch import search as google_search


class Tools:
    @staticmethod
    async def sherlock(username):
        try:
            process = await asyncio.create_subprocess_exec(
                "sherlock",
                username,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                output = stdout.decode("utf-8", errors="replace")
            else:
                output = stderr.decode("utf-8", errors="replace")

            return output

        except Exception as e:
            print(f"Exceção ao executar sherlock para {username}: {e}")


    @staticmethod
    async def holehe(email):
        try:
            process = await asyncio.create_subprocess_exec(
                "holehe",
                email,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                output = stdout.decode("utf-8", errors="replace")
            else:
                output = stderr.decode("utf-8", errors="replace")

            return output

        except Exception as e:
            print(f"Exceção ao executar holehe para {email}: {e}")


    @staticmethod
    async def search(query):
        try:
            results = await asyncio.to_thread(
                lambda: list(
                    google_search(query, num_results=10)
                )
            )

            output = "\n".join(results)

            return output

        except Exception as e:
            print(f"Exceção ao executar pesquisa para {query}: {e}")
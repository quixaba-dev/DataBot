# cli.py
import utils.logging
import asyncio
from core.agent import Agent
from providers.openaicompatible import OpenAICompatible
import os


async def main():
    agent = Agent(OpenAICompatible())

    os.system("cls")
    print("DataCenter AI CLI")
    print("Digite 'exit' para sair.\n\n\n")

    while True:
        
        prompt = await asyncio.to_thread(
            input,
            "> "
        )

        if prompt.strip().lower() in {"exit", "quit"}:
            break

        if not prompt.strip():
            continue

        try:
            result = await agent.query(prompt)

            print()
            print(result["response"])
            print()

        except Exception as e:
            print(f"\nErro: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
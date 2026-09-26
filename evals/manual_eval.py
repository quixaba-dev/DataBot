import asyncio
import time
from pathlib import Path

from core.agent import Agent
from providers.openaicompatible import OpenAICompatible


PROMPTS = [
    """
Analise o comportamento de mercado da Kitsune nos anúncios disponíveis.
Não quero apenas seu valor: identifique o que as pessoas costumam oferecer
ou pedir por ela, quais itens aparecem associados, como sua demanda influencia
as negociações e se existem sinais de que os traders exigem prêmio para
negociá-la. Justifique usando padrões encontrados nos anúncios.
""",

    """
Compare Kitsune, Magnet e Control como ativos de trading.
Analise demanda, liquidez aparente, frequência nas ofertas, capacidade de
conseguir upgrades e tipos de itens pelos quais os jogadores parecem dispostos
a trocá-los. Explique por que itens com valores diferentes podem apresentar
comportamentos diferentes no mercado.
""",

    """
Investigue os anúncios classificados como Overpay e Underpay.
Procure padrões que expliquem por que uma troca recebe essas classificações.
O valor total é suficiente para explicar o fenômeno ou demanda, quantidade
de itens, raridade, Limiteds e outros fatores parecem influenciar?
Diferencie observações de conclusões.
""",

    """
Analise o papel da demanda no mercado.
Compare itens com demanda alta e baixa e observe se itens de alta demanda
conseguem ser negociados por valores nominais maiores, bundles diferentes
ou itens mais raros. Existem casos em que um item de menor valor parece
comercialmente mais desejável que outro de maior valor?
""",

    """
Quero transformar meu inventário em itens cada vez mais valiosos através
de upgrades. Com base exclusivamente nos anúncios recuperados, identifique
quais características parecem tornar um item bom para esse tipo de estratégia.
Analise demanda, quantidade de itens, combinações e comportamento dos traders.
Explique a lógica observada em vez de apenas listar valores.
""",

    """
Compare o comportamento de frutas Regular (R), Permanent (P), Limiteds
e Gamepasses. Investigue se cada categoria parece cumprir um papel diferente
nas negociações, como reserva de valor, complemento de trade, alvo de upgrade
ou item de alta procura. Indique quando os dados forem insuficientes.
""",

    """
Investigue o mercado de Dragon nos anúncios disponíveis, separando
East Dragon, West Dragon e suas versões Regular e Permanent quando existirem.
Analise quais itens aparecem ao redor dessas negociações, diferenças de demanda,
valor, tamanho dos bundles e comportamento de quem procura ou oferece Dragon.
""",

    """
Procure fenômenos de mercado que não sejam imediatamente visíveis olhando
apenas a tabela de valores. Investigue preferência por liquidez, prêmio por
demanda, consolidação de vários itens em um item maior, diferença entre valor
nominal e percebido, preferência por Limiteds e resistência a determinados itens.
Mostre quais observações sustentam cada hipótese.
""",

    """
Imagine que os valores oficiais fossem removidos e você tivesse somente
os anúncios de trading. Até que ponto seria possível reconstruir uma hierarquia
aproximada de valor e desejo dos itens observando o que jogadores oferecem e
solicitam? Diferencie conclusões fortes, hipóteses e coisas impossíveis de
determinar com a amostra disponível.
""",

    """
Faça uma análise geral da microeconomia representada pelos anúncios recuperados.
Identifique padrões de liquidez, demanda, prêmio, concentração de valor,
upgrades, bundles e diferenças entre valor listado e preferência dos traders.

Organize sua análise separando claramente:

1. fatos diretamente observados;
2. padrões recorrentes;
3. hipóteses econômicas;
4. coisas que os dados não permitem concluir.

Explique também como esses fatores podem interagir e produzir mudanças
no comportamento do mercado ao longo do tempo.
"""
]


agent = Agent(provider=OpenAICompatible())


async def main():

    output = Path("resultados_teste.txt")

    output.write_text(
        "AVALIAÇÃO MANUAL DO AGENTE\n"
        "========================\n\n",
        encoding="utf-8"
    )

    for numero, prompt in enumerate(PROMPTS, start=1):

        prompt = prompt.strip()

        print("\n" + "=" * 80)
        print(f"TESTE {numero}/{len(PROMPTS)}")
        print("=" * 80)

        print("\nPROMPT:")
        print(prompt)

        print("\nRESPOSTA:\n")

        inicio = time.perf_counter()

        try:
            resultado = await agent.query(prompt)

            tempo = time.perf_counter() - inicio

            resposta = resultado["response"]
            contexto = resultado["context"]
            quantidade = resultado["document_count"]
            caracteres = resultado["context_characters"]

        except Exception as e:

            tempo = time.perf_counter() - inicio

            resposta = (
                f"ERRO: {type(e).__name__}: {e}"
            )

            contexto = "Contexto indisponível devido ao erro."
            quantidade = 0
            caracteres = 0

        with output.open(
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"""
{'=' * 80}
TESTE {numero}
{'=' * 80}

PROMPT:

{prompt}


-------------------- RAG DEBUG --------------------

DOCUMENTOS RECUPERADOS:
{quantidade}

CARACTERES DO CONTEXTO:
{caracteres:,}

CONTEXTO ENVIADO AO MODELO:

{contexto}

-------------------- FIM DO CONTEXTO --------------------


RESPOSTA:

{resposta}


TEMPO:
{tempo:.2f}s


"""
            )

        print(resposta)
        print(f"\nDocumentos: {quantidade}")
        print(f"Contexto: {caracteres:,} caracteres")
        print(f"Tempo: {tempo:.2f}s")

        await asyncio.sleep(1)

    print("\n" + "=" * 80)
    print("TESTES FINALIZADOS")
    print("=" * 80)

    print(
        f"\nResultados salvos em: {output.resolve()}"
    )


if __name__ == "__main__":
    asyncio.run(main())

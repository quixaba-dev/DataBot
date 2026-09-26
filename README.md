<div align="center">

# 🧠 DataCenter AI

### Discord AI Agent for Blox Fruits Market Analysis

**RAG · Semantic Search · Tool Calling · OSINT**

<br>

<p>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white">
  <img src="https://img.shields.io/badge/Groq-AI-F55036?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Experimental-orange?style=for-the-badge">
</p>

Bot experimental para Discord que combina **IA, RAG e busca semântica** para analisar dados do mercado de trocas de **Blox Fruits**.

</div>

---

## ✨ Sobre

O **DataCenter AI** é um agente experimental desenvolvido em Python para responder perguntas e analisar padrões relacionados ao mercado de trocas de **Blox Fruits**.

O projeto combina um LLM acessado através da **Groq**, busca semântica local utilizando **Sentence Transformers + FAISS** e um sistema de **Tool Calling** capaz de executar ferramentas externas quando necessário.

Os dados são armazenados localmente em arquivos JSONL, processados e transformados em embeddings durante a inicialização.

---

## 🚀 Funcionalidades

- 🎮 Integração com **Discord** através do comando `.transcend`
- 🧠 **RAG** para recuperação de contexto
- 🔎 Embeddings com `all-MiniLM-L6-v2`
- ⚡ Busca vetorial em memória com **FAISS**
- 📊 Análise de anúncios e valores de itens
- 🛠️ **Tool Calling** controlado pelo modelo
- 🕵️ Integração com **Sherlock** e **Holehe**
- 📝 Sistema centralizado de **logging**
- 🧪 Ambiente de avaliação manual do agente
- 💬 Divisão automática de respostas para respeitar o limite do Discord

> **Importante:** registros `trade_listing` representam anúncios encontrados no conjunto de dados, não trocas confirmadas. Valores, demanda e outros rótulos representam informações presentes nas fontes utilizadas e não necessariamente negociações efetivamente realizadas.

---

## ⚙️ Como funciona

```text
Discord (.transcend)
        │
        ▼
   ┌─────────┐
   │  Agent  │
   └────┬────┘
        │
        ├──────────────► RAG
        │                 │
        │            Semantic Search
        │                 │
        │                FAISS
        │                 │
        │              JSONL Data
        │                 │
        ◄──── Context ─────┘
        │
        ▼
   Groq / LLM
        │
        ├──► Tool Call?
        │        │
        │        ▼
        │   ┌─────────────┐
        │   │ Tool Caller │
        │   └──────┬──────┘
        │          │
        │     ┌────┴────┐
        │     ▼         ▼
        │  Sherlock   Holehe
        │
        ▼
     Response
        │
        ▼
     Discord
```

Quando uma pergunta é enviada, o agente recupera até **15 documentos semanticamente relevantes** e adiciona esse conteúdo ao contexto enviado ao modelo.

O modelo também pode solicitar a execução das tools disponíveis antes de produzir a resposta final.

---

## 🧩 RAG

<div align="center">

<img src="https://img.shields.io/badge/Sentence_Transformers-all--MiniLM--L6--v2-yellow?style=flat-square">
<img src="https://img.shields.io/badge/FAISS-Vector_Search-0467DF?style=flat-square">
<img src="https://img.shields.io/badge/JSONL-Local_Data-lightgrey?style=flat-square">

</div>

<br>

O sistema percorre automaticamente:

```text
data/**/*.jsonl
```

Durante a inicialização, os documentos são formatados, transformados em embeddings e adicionados a um índice **FAISS mantido em memória**.

Linhas vazias e registros:

```json
{
  "type": "metadata"
}
```

são ignorados durante a indexação.

### Dados

A pasta `data/` está ignorada pelo Git e **não acompanha o repositório**.

Antes de iniciar o projeto, forneça seus próprios arquivos:

```text
data/
├── values.jsonl
├── trades.jsonl
└── ...
```

Cada linha deve conter um objeto JSON válido.

---

## 🔧 Tools

O DataCenter AI possui um sistema de tools que podem ser selecionadas automaticamente pelo modelo.

| Tool | Função |
| --- | --- |
| 🔎 **Sherlock** | Procura um username em diferentes serviços e plataformas |
| 📧 **Holehe** | Consulta serviços associados a um endereço de e-mail |

Os esquemas e o roteamento ficam em:

```text
tools/ToolCaller.py
```

enquanto suas implementações ficam em:

```text
tools/tools.py
```

> Uma ferramenta de busca web também está implementada em `tools/tools.py`, mas atualmente não está exposta ao modelo pelo `ToolCaller`.

---

## 🛠️ Tech Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=python,discord,git,github,vscode" alt="Tech Stack">

<br><br>

<img src="https://img.shields.io/badge/Groq-LLM_API-F55036?style=flat-square">
<img src="https://img.shields.io/badge/FAISS-Vector_Search-0467DF?style=flat-square">
<img src="https://img.shields.io/badge/Sentence_Transformers-Embeddings-yellow?style=flat-square">
<img src="https://img.shields.io/badge/AsyncIO-Asynchronous-3776AB?style=flat-square&logo=python&logoColor=white">

</div>

---

## 📁 Estrutura

```text
DataCenter-AI/
│
├── bot/
│   └── rules.txt              # Instruções e formato das respostas
│
├── core/
│   ├── agent.py               # Groq, contexto e fluxo de Tool Calling
│   ├── bot.py                 # Discord e comando .transcend
│   └── rag.py                 # JSONL, embeddings, FAISS e busca
│
├── data/                      # Dados locais (ignorado pelo Git)
│   └── *.jsonl
│
├── evals/
│   └── manual_eval.py         # Avaliação exploratória do agente
│
├── tools/
│   ├── ToolCaller.py          # Esquemas e roteamento das tools
│   └── tools.py               # Implementações das tools
│
├── utils/
│   └── logging.py             # Configuração centralizada de logs
│
├── config.py                  # Variáveis de ambiente
├── main.py                    # Entry point
└── requirements.txt
```

---

## 📦 Requisitos

- **Python 3.11+**
- Token do Discord
- Chave da API da Groq
- Arquivos JSONL dentro de `data/`
- `sherlock` disponível no `PATH`
- `holehe` disponível no `PATH`

As dependências Python estão disponíveis em [`requirements.txt`](requirements.txt).

O modelo utilizado pelo Sentence Transformers pode ser baixado automaticamente durante a primeira execução.

---

## 🚀 Instalação

### 1. Clone o projeto

```bash
git clone <URL_DO_REPOSITORIO>
cd DataCenter-AI
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o ambiente

Copie `.env.example` para `.env` e defina:

```dotenv
TOKEN=seu_token_do_discord
OPENAI_API_KEY=sua_chave_da_groq
```

> Apesar do nome `OPENAI_API_KEY`, o cliente utiliza o endpoint compatível com OpenAI disponibilizado pela Groq.

### 5. Adicione os dados

Coloque seus arquivos `.jsonl` dentro de:

```text
data/
```

Subpastas também são suportadas.

### 6. Inicie

```bash
python main.py
```

> Execute o projeto a partir da raiz do repositório. Os caminhos de `data/` e `bot/rules.txt` são relativos ao diretório atual.

Os dados precisam estar disponíveis **antes da inicialização**, pois os embeddings e o índice FAISS são criados durante a importação de `core.rag`.

---

## 💬 Uso

No Discord:

```text
.transcend Analise os anúncios de Kitsune e os itens oferecidos por ela.
```

O agente recupera os documentos semanticamente mais relevantes, utiliza os resultados como contexto e envia a solicitação ao modelo.

As respostas são encaminhadas ao canal em partes de até **2.000 caracteres**.

---

## 🧪 Avaliação manual

O projeto inclui um pequeno ambiente de avaliação em:

```text
evals/manual_eval.py
```

Ele executa uma coleção de prompts analíticos contra o agente e registra informações como respostas, contexto recuperado e métricas em:

```text
resultados_teste.txt
```

Esse script é destinado à **avaliação exploratória e humana do comportamento do agente**, não sendo uma suíte automatizada de testes.

---

## 📝 Logging

O projeto utiliza logging centralizado através de:

```text
utils/logging.py
```

Os diferentes módulos podem registrar informações de execução e diagnóstico sem depender de `print()`, facilitando a análise do fluxo do agente e principalmente do processo de recuperação do RAG.

---

## 🤖 Configuração do agente

| Arquivo | Responsabilidade |
| --- | --- |
| `bot/rules.txt` | Instruções e formato esperado das respostas |
| `core/agent.py` | Modelo, contexto e processamento das queries |
| `core/rag.py` | Recuperação e indexação dos dados |
| `tools/ToolCaller.py` | Definição das tools disponíveis |
| `tools/tools.py` | Implementação das tools |
| `utils/logging.py` | Configuração do sistema de logs |

O modelo padrão utilizado atualmente é:

```text
openai/gpt-oss-120b
```

---

## ⚠️ Limitações atuais

- O índice FAISS existe apenas em memória e é reconstruído durante a inicialização.
- Os dados locais não acompanham o repositório.
- O projeto ainda utiliza caminhos relativos ao diretório de execução.
- A busca web existe na implementação, mas ainda não está exposta ao modelo através do `ToolCaller`.
- O ambiente em `evals/` realiza avaliação manual, não testes automatizados.

O projeto utiliza `discord.py-self` com `self_bot=True`, automatizando uma conta de usuário. Verifique os termos atuais da plataforma antes de utilizar uma conta real.

---

## 🚧 Status

> **Experimental / Em desenvolvimento**

O DataCenter AI continua evoluindo. O sistema RAG, ferramentas, conjunto de dados e processo de avaliação podem mudar conforme novos experimentos são realizados.

---

<div align="center">

### 🧠 DataCenter AI

**Turning market data into context.**

`Discord` • `Groq` • `RAG` • `FAISS` • `Tool Calling`

<br><br>

Built with Python 🐍

</div>
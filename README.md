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

Bot experimental para Discord que utiliza **IA + RAG** para analisar dados e responder perguntas sobre o mercado de trocas do **Blox Fruits**.

</div>

---

## ✨ Sobre

O **DataCenter AI** é um agente experimental desenvolvido em Python para analisar informações relacionadas ao mercado de trocas do **Blox Fruits**.

O projeto combina um LLM acessado através da **Groq**, busca semântica local utilizando **Sentence Transformers + FAISS** e um sistema de **Tool Calling** capaz de executar ferramentas externas.

Os dados são armazenados localmente em arquivos JSONL e transformados em embeddings, permitindo que o agente recupere informações relevantes antes de gerar uma resposta.

```text
Discord
   │
   ▼
Agent
   │
   ├────────► RAG ────────► FAISS
   │                         │
   │                    Dados JSONL
   │
   ├────────► LLM (Groq)
   │
   └────────► Tool Caller
                    │
              ┌─────┴─────┐
              ▼           ▼
          Sherlock      Holehe
```

---

## 🚀 Funcionalidades

- 🎮 Integração com **Discord**
- 🧠 RAG com busca semântica local
- 🔎 Embeddings com `all-MiniLM-L6-v2`
- ⚡ Índice vetorial utilizando **FAISS**
- 📊 Análise de anúncios e valores de itens
- 🛠️ Tool Calling controlado pelo modelo
- 🕵️ Integração com **Sherlock** e **Holehe**
- 💬 Respostas automaticamente divididas para respeitar o limite do Discord
- 📁 Carregamento automático de dados JSONL

> **Importante:** registros `trade_listing` representam anúncios encontrados no conjunto de dados. Eles não confirmam que uma troca foi efetivamente concluída.

---

## ⚙️ Como funciona

Quando uma pergunta é enviada através do comando:

```text
.transcend <pergunta>
```

o DataCenter AI executa aproximadamente o seguinte fluxo:

```text
Pergunta
   │
   ▼
Discord Bot
   │
   ▼
Agent
   │
   ├──► Semantic Search
   │        │
   │        ▼
   │      FAISS
   │        │
   │   Top 15 documentos
   │        │
   ◄────────┘
   │
   ▼
Contexto + Pergunta
   │
   ▼
LLM
   │
   ├──► Tool necessária? ──► Tool Caller
   │
   ▼
Resposta
   │
   ▼
Discord
```

O agente recupera até **15 documentos relevantes**, adiciona o conteúdo encontrado ao contexto e envia a solicitação ao modelo.

Quando necessário, o próprio modelo também pode solicitar a execução das tools disponíveis.

---

## 🧩 RAG

O sistema de recuperação utiliza:

<div align="center">

<img src="https://img.shields.io/badge/Sentence_Transformers-all--MiniLM--L6--v2-yellow?style=flat-square">
<img src="https://img.shields.io/badge/FAISS-Vector_Search-blue?style=flat-square">
<img src="https://img.shields.io/badge/JSONL-Local_Data-lightgrey?style=flat-square">

</div>

<br>

Os documentos são carregados automaticamente de:

```text
data/**/*.jsonl
```

Cada linha deve conter um objeto JSON válido.

Registros com:

```json
{
  "type": "metadata"
}
```

são ignorados durante a indexação.

Os demais registros são formatados, transformados em embeddings e adicionados ao índice FAISS em memória.

### Dados

A pasta `data/` **não faz parte do repositório** e está ignorada pelo Git.

Portanto, antes de iniciar o bot, você deve fornecer seus próprios arquivos:

```text
data/
├── values.jsonl
├── trades.jsonl
└── ...
```

---

## 🔧 Tools

O agente possui ferramentas externas que podem ser selecionadas automaticamente pelo modelo.

| Tool | Função |
| --- | --- |
| 🔎 **Sherlock** | Procura um username em diferentes serviços e plataformas |
| 📧 **Holehe** | Consulta serviços possivelmente associados a um endereço de e-mail |

As definições das ferramentas ficam em:

```text
tools/ToolCaller.py
```

e suas implementações em:

```text
tools/tools.py
```

A arquitetura permite adicionar novas tools ao agente sem alterar seu fluxo principal.

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
│   ├── agent.py               # Agent, Groq, RAG e Tool Calling
│   ├── bot.py                 # Discord bot e comando .transcend
│   └── rag.py                 # JSONL, embeddings, FAISS e busca
│
├── data/                      # Dados locais (ignorado pelo Git)
│   └── *.jsonl
│
├── tools/
│   ├── ToolCaller.py          # Definições e roteamento das tools
│   └── tools.py               # Sherlock, Holehe e outras tools
│
├── config.py                  # Variáveis de ambiente
├── main.py                    # Entry point
├── requirements.txt
└── test.py                    # Consultas exploratórias
```

---

## 📦 Requisitos

- **Python 3.11+**
- Token do Discord
- Chave da API da Groq
- `sherlock` disponível no `PATH`
- `holehe` disponível no `PATH`
- Arquivos JSONL em `data/`

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

### 4. Configure as variáveis

Copie:

```text
.env.example
```

para:

```text
.env
```

e configure:

```dotenv
TOKEN=seu_token_do_discord
OPENAI_API_KEY=sua_chave_da_groq
```

> Apesar do nome `OPENAI_API_KEY`, o cliente utiliza a API compatível com OpenAI disponibilizada pela Groq.

### 5. Adicione os dados

Coloque os arquivos `.jsonl` dentro de:

```text
data/
```

Subpastas também são suportadas.

### 6. Inicie

```bash
python main.py
```

Execute o comando a partir da **raiz do projeto**, pois alguns caminhos utilizados pela aplicação são relativos ao diretório atual.

---

## 💬 Uso

No Discord:

```text
.transcend Qual é o comportamento dos anúncios de Kitsune?
```

O agente pesquisa o conjunto de dados, recupera os registros semanticamente mais relevantes e utiliza essas informações como contexto para gerar a resposta.

---

## 🤖 Configuração do agente

O comportamento do agente pode ser personalizado através de:

| Arquivo | Responsabilidade |
| --- | --- |
| `bot/rules.txt` | Instruções e formato das respostas |
| `core/agent.py` | Modelo, agente e processamento das queries |
| `core/rag.py` | Recuperação e indexação dos dados |
| `tools/ToolCaller.py` | Definição das tools disponíveis |
| `tools/tools.py` | Implementação das tools |

O modelo padrão utilizado atualmente é:

```text
openai/gpt-oss-120b
```

---

## ⚠️ Observações

O índice FAISS e os embeddings são criados durante a importação de `core.rag`. Por isso, os arquivos JSONL precisam estar disponíveis **antes** da execução de `main.py`.

`test.py` contém consultas exploratórias utilizadas para analisar o comportamento do agente e do conjunto de dados. Ele **não é uma suíte automatizada de testes**.

O projeto utiliza `discord.py-self` com `self_bot=True`. Esse modo automatiza uma conta de usuário e pode estar sujeito às restrições e aos termos da plataforma.

---

## 🚧 Status

> **Experimental / Em desenvolvimento**

O DataCenter AI ainda está evoluindo. A arquitetura, sistema RAG, conjunto de dados e ferramentas podem sofrer mudanças conforme novos experimentos são realizados.

---

<div align="center">

### 🧠 DataCenter AI

**Turning market data into context.**

`Discord` • `Groq` • `RAG` • `FAISS` • `Tool Calling`

<br>

Built with Python 🐍

</div>
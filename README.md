<div align="center">

# 🧠 DataCenter AI

### Context-Aware AI Agent with RAG & Tool Calling

**RAG · Semantic Search · Tool Calling · Extensible Context**

<br>

<p>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white">
  <img src="https://img.shields.io/badge/Groq-AI-F55036?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Experimental-orange?style=for-the-badge">
</p>

Agente de IA extensível capaz de combinar **contexto externo, recuperação semântica e ferramentas** para responder perguntas e executar tarefas.

</div>

---

## ✨ Sobre

O **DataCenter AI** é um agente experimental desenvolvido em Python com foco em **contexto extensível e integração de ferramentas**.

Em vez de limitar o modelo ao conhecimento disponível no próprio LLM, o projeto permite alimentar o agente com informações provenientes de fontes externas. Esses dados são indexados e recuperados semanticamente através de uma arquitetura **RAG (Retrieval-Augmented Generation)**.

O agente também possui suporte a **Tool Calling**, permitindo que novas ferramentas sejam disponibilizadas ao modelo para ampliar suas capacidades além da geração de texto.

A arquitetura busca manter três responsabilidades independentes:

```text
Context Sources  →  conhecimento disponível ao agente
Tools            →  capacidades disponíveis ao agente
Interfaces       →  onde o agente pode ser utilizado
```

Os dados e ferramentas presentes atualmente no repositório são **implementações e fontes utilizadas pelo projeto**, e não definem o propósito ou domínio do DataCenter AI.

---

## 🚀 Funcionalidades

- 🧠 **RAG** para enriquecimento dinâmico de contexto
- 🔎 Busca semântica baseada em embeddings
- ⚡ Indexação vetorial utilizando **FAISS**
- 📁 Suporte a fontes de contexto baseadas em JSONL
- 🛠️ Arquitetura de **Tool Calling**
- 🧩 Sistema extensível de tools
- 🤖 Integração com LLM através da **Groq**
- 🎮 Interface atual através do **Discord**
- ⚡ Processamento assíncrono
- 📝 Sistema centralizado de logging
- 🧪 Ambiente para avaliação manual do agente

---

## 🏗️ Arquitetura

```text
                         ┌─────────────────┐
                         │    Interface    │
                         │     Discord     │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │      Agent      │
                         └────────┬────────┘
                                  │
                   ┌──────────────┴──────────────┐
                   │                             │
                   ▼                             ▼
          ┌─────────────────┐           ┌─────────────────┐
          │       RAG       │           │   Tool Caller   │
          └────────┬────────┘           └────────┬────────┘
                   │                             │
                   ▼                             ▼
          ┌─────────────────┐           ┌─────────────────┐
          │ Semantic Search │           │      Tools      │
          │      FAISS      │           │                 │
          └────────┬────────┘           └─────────────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Context Sources │
          └─────────────────┘
```

O **Agent** funciona como núcleo da aplicação.

Ele recebe uma solicitação através da interface disponível, recupera informações relevantes das fontes de contexto e envia a pergunta enriquecida ao modelo.

Quando necessário, o modelo também pode solicitar a execução das tools disponibilizadas pelo sistema.

---

## 🧠 Contexto e RAG

O DataCenter AI foi projetado para permitir que conhecimento externo seja incorporado ao agente sem precisar fazer parte do modelo utilizado.

Atualmente, a implementação utiliza:

<div align="center">

<img src="https://img.shields.io/badge/Sentence_Transformers-all--MiniLM--L6--v2-yellow?style=flat-square">
<img src="https://img.shields.io/badge/FAISS-Vector_Search-0467DF?style=flat-square">
<img src="https://img.shields.io/badge/JSONL-Context_Source-lightgrey?style=flat-square">

</div>

<br>

Os documentos atuais são carregados de:

```text
data/**/*.jsonl
```

Cada registro válido é formatado e convertido em um embedding utilizando `all-MiniLM-L6-v2`.

Os vetores resultantes são armazenados em um índice **FAISS em memória**, permitindo recuperar documentos semanticamente relacionados à solicitação do usuário.

O agente atualmente recupera até **15 documentos relevantes** para compor seu contexto.

### Fontes de dados

A pasta `data/` representa as **fontes de contexto atualmente utilizadas**, não um domínio fixo do projeto.

```text
data/
├── source_1.jsonl
├── source_2.jsonl
└── ...
```

A pasta está ignorada pelo Git, portanto os dados não acompanham o repositório.

Registros com:

```json
{
  "type": "metadata"
}
```

são ignorados durante a indexação.

> O conteúdo presente em `data/` determina parte do conhecimento externo disponível ao agente, mas não altera o propósito geral do sistema.

---

## 🔧 Tool Calling

Além de receber contexto externo, o agente pode utilizar **tools** para executar operações que um LLM sozinho não conseguiria realizar.

O fluxo básico é:

```text
User Request
     │
     ▼
   Agent
     │
     ▼
    LLM
     │
     ▼
Tool required?
   │       │
  Yes      No
   │       │
   ▼       │
Tool Caller│
   │       │
   ▼       │
   Tool    │
   │       │
   └───┬───┘
       ▼
    Response
```

As tools disponíveis são declaradas em:

```text
tools/ToolCaller.py
```

e implementadas em:

```text
tools/tools.py
```

Atualmente existem integrações como **Sherlock** e **Holehe**, além de uma implementação de busca web ainda não exposta ao modelo.

Essas ferramentas são apenas capacidades atualmente conectadas ao agente. A arquitetura permite que outras tools sejam adicionadas conforme a necessidade.

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
│   └── rules.txt              # Instruções do agente
│
├── core/
│   ├── agent.py               # Orquestração do agente e LLM
│   ├── bot.py                 # Interface Discord
│   └── rag.py                 # Recuperação e indexação de contexto
│
├── data/                      # Fontes locais de contexto
│   └── *.jsonl
│
├── evals/
│   └── manual_eval.py         # Avaliação exploratória do agente
│
├── tools/
│   ├── ToolCaller.py          # Definições e roteamento das tools
│   └── tools.py               # Implementações das tools
│
├── utils/
│   └── logging.py             # Configuração centralizada de logs
│
├── config.py                  # Configuração do ambiente
├── main.py                    # Entry point
└── requirements.txt
```

---

## 📦 Requisitos

- **Python 3.11+**
- Token do Discord
- Chave da API da Groq
- Fontes de contexto em `data/`
- Dependências definidas em `requirements.txt`

Tools externas podem possuir requisitos adicionais. Por exemplo, as integrações atuais com Sherlock e Holehe exigem seus respectivos executáveis disponíveis no `PATH`.

---

## 🚀 Instalação

### 1. Clone o repositório

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

Copie `.env.example` para `.env`:

```dotenv
TOKEN=seu_token_do_discord
OPENAI_API_KEY=sua_chave_da_groq
```

Apesar do nome `OPENAI_API_KEY`, o cliente atual utiliza o endpoint compatível com OpenAI disponibilizado pela Groq.

### 5. Adicione fontes de contexto

Adicione os arquivos JSONL desejados em:

```text
data/
```

Os dados precisam estar disponíveis antes da inicialização, pois os embeddings e o índice FAISS são construídos durante o carregamento de `core.rag`.

### 6. Inicie

```bash
python main.py
```

---

## 💬 Uso

A interface atual do projeto é o Discord.

```text
.transcend <pergunta>
```

Por exemplo:

```text
.transcend Analise as informações disponíveis sobre este assunto.
```

O agente recupera contexto semanticamente relacionado à pergunta, fornece essas informações ao modelo e disponibiliza as tools configuradas para aquela execução.

As respostas são divididas automaticamente em partes de até **2.000 caracteres** antes de serem enviadas ao Discord.

---

## 🧪 Avaliação

O projeto possui um ambiente de avaliação manual em:

```text
evals/manual_eval.py
```

Ele permite executar conjuntos de prompts contra o agente e analisar seu comportamento, contexto recuperado e respostas.

O script é destinado a **avaliação exploratória**, não sendo uma suíte automatizada de testes.

---

## 📝 Logging

A configuração centralizada de logging fica em:

```text
utils/logging.py
```

Os módulos utilizam loggers próprios para registrar eventos e informações de diagnóstico sem depender de `print()`.

Isso permite acompanhar separadamente componentes como Agent, RAG, interfaces e tools durante a execução.

---

## ⚙️ Configuração

| Arquivo | Responsabilidade |
| --- | --- |
| `bot/rules.txt` | Comportamento e instruções do agente |
| `core/agent.py` | Orquestração do modelo e contexto |
| `core/rag.py` | Recuperação e indexação |
| `core/bot.py` | Interface Discord |
| `tools/ToolCaller.py` | Tools disponibilizadas ao modelo |
| `tools/tools.py` | Implementação das tools |
| `utils/logging.py` | Configuração dos logs |

O modelo padrão utilizado atualmente é:

```text
openai/gpt-oss-120b
```

---

## ⚠️ Limitações atuais

- O índice FAISS é mantido em memória e reconstruído na inicialização.
- A implementação atual de contexto utiliza arquivos JSONL.
- Os dados em `data/` não acompanham o repositório.
- Alguns caminhos ainda são relativos ao diretório de execução.
- A busca web implementada ainda não está exposta ao modelo.
- O ambiente de `evals/` realiza avaliação manual, não testes automatizados.

A interface atual utiliza `discord.py-self` com `self_bot=True`, automatizando uma conta de usuário. Verifique os termos atuais da plataforma antes de utilizar uma conta real.

---

## 🚧 Status

> **Experimental / Em desenvolvimento**

O DataCenter AI está sendo desenvolvido como uma arquitetura extensível para agentes capazes de combinar **LLMs, contexto externo e ferramentas**.

Novas fontes de contexto, interfaces, estratégias de recuperação e tools podem ser incorporadas conforme o projeto evolui.

---

<div align="center">

### 🧠 DataCenter AI

**Context in. Intelligence out.**

`LLM` • `RAG` • `Semantic Search` • `Tool Calling`

<br><br>

Built with Python 🐍

</div>
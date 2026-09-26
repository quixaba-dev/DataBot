<div align="center">

# 🤖 DataBot

**Assistente inteligente para Telegram com RAG, tools extensíveis e API assíncrona.**

<p>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-API-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  <img src="https://img.shields.io/badge/AI-RAG-8A2BE2?style=for-the-badge" alt="RAG">
</p>

Sistema modular que combina **Inteligência Artificial**, **Retrieval-Augmented Generation (RAG)** e **tools externas** para fornecer respostas contextuais e executar tarefas diretamente pelo Telegram.

</div>

---

## Sobre o projeto

O **DataBot** é um bot de Telegram desenvolvido em Python que utiliza uma arquitetura baseada em **RAG (Retrieval-Augmented Generation)** para enriquecer as respostas da IA com informações recuperadas de fontes externas.

Além da interface pelo Telegram, o projeto possui uma **API Flask** para receber e processar queries de forma independente.

A arquitetura foi projetada pensando principalmente em **modularidade e extensibilidade**, permitindo adicionar novas tools ao agente sem precisar alterar toda a estrutura do projeto.

---

## Funcionalidades

- 🤖 **Integração com Telegram** — interação direta com o agente através do bot.
- 🧠 **RAG** — recuperação de contexto relevante antes da geração da resposta.
- 🔧 **Tool Calling** — o agente pode selecionar e executar ferramentas quando necessário.
- 🕵️ **OSINT** — integração com ferramentas como Sherlock e Holehe.
- 🌐 **API Flask** — endpoint independente para processamento de queries.
- ⚡ **Processamento assíncrono** — operações de IA e tools utilizando fluxo assíncrono.
- 🧩 **Arquitetura modular** — novas ferramentas podem ser adicionadas facilmente.

---

## Arquitetura

```text
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
          ┌──────▼──────┐         ┌──────▼──────┐
          │ Telegram Bot│         │  Flask API  │
          └──────┬──────┘         └──────┬──────┘
                 │                       │
                 └───────────┬───────────┘
                             │
                      ┌──────▼──────┐
                      │    Agent    │
                      └──────┬──────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
          ┌──────▼──────┐         ┌──────▼──────┐
          │     RAG     │         │ Tool Caller │
          └─────────────┘         └──────┬──────┘
                                         │
                              ┌──────────▼──────────┐
                              │   External Tools   │
                              │ Sherlock · Holehe │
                              └─────────────────────┘
```

O **Agent** funciona como núcleo do sistema. Ele recebe as mensagens vindas do Telegram ou da API, recupera contexto através do RAG e pode acionar tools externas quando necessário.

---

## Tools

O DataBot possui um sistema de ferramentas plugáveis que permite expandir as capacidades do agente.

| Tool | Função |
|---|---|
| 🔎 **Sherlock** | Busca usernames em diversas plataformas |
| 📧 **Holehe** | Verifica serviços associados a um endereço de e-mail |
| 🧩 **Custom Tools** | Novas ferramentas podem ser integradas ao sistema |

A arquitetura permite adicionar novas tools sem modificar diretamente o funcionamento principal do agente.

---

## Tech Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=python,flask,git,github,vscode" alt="Tech Stack">

<br><br>

<img src="https://img.shields.io/badge/Telegram_Bot_API-26A5E4?style=flat-square&logo=telegram&logoColor=white">
<img src="https://img.shields.io/badge/RAG-Retrieval_Augmented_Generation-8A2BE2?style=flat-square">
<img src="https://img.shields.io/badge/AsyncIO-Asynchronous-3776AB?style=flat-square&logo=python&logoColor=white">

</div>

---

## Estrutura

```text
DataBot/
│
├── bot/
│   ├── rules.txt
│   └── ...
│
├── core/
│   └── rag.py
│
├── tools/
│   ├── ToolCaller.py
│   └── ...
│
├── agent.py
├── api.py
└── main.py
```

> A estrutura pode mudar conforme novas funcionalidades e integrações forem adicionadas ao projeto.

---

## Fluxo de uma requisição

```text
Usuário
   ↓
Telegram / API
   ↓
Agent
   ↓
RAG ──────→ Recuperação de contexto
   ↓
LLM
   ↓
Tool necessária?
   ├── Sim → Tool Caller → Tool → Resultado
   └── Não
   ↓
Resposta
   ↓
Usuário
```

---

## Objetivo

O objetivo do **DataBot** é servir como uma base modular para construção de agentes de IA capazes de combinar:

**LLMs + RAG + Tool Calling + APIs + OSINT**

A estrutura prioriza facilidade de expansão, permitindo que novas fontes de dados, integrações e ferramentas sejam incorporadas conforme o projeto evolui.

---

## Status

> 🚧 **Em desenvolvimento**

O projeto ainda está evoluindo e novas funcionalidades, tools e melhorias na arquitetura serão adicionadas progressivamente.

---

<div align="center">

**DataBot** · Built with Python 🐍

</div>

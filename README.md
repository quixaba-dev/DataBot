# DataBot 🤖

Bot de Telegram com Inteligência Artificial baseada em RAG, API Flask assíncrona e sistema extensível de tools.

---

## 🚀 Sobre o projeto

O **DataBot** é um bot para Telegram que utiliza IA com arquitetura **RAG (Retrieval-Augmented Generation)** para gerar respostas contextuais e mais precisas.

O sistema também conta com uma API em **Flask** para processamento de queries, funcionando de forma assíncrona com threads separadas entre o bot e a API.

---

## ⚙️ Funcionalidades

- 🤖 Bot integrado ao Telegram
- 🧠 IA com sistema RAG (contexto + recuperação de dados)
- 🌐 API em Flask para receber queries
- 🔄 Processamento assíncrono com threads
- 🧩 Sistema modular de tools
- 🕵️ Tools OSINT integradas (Sherlock, Holehe, etc.)
- ➕ Facilidade para adicionar novas tools ao sistema

---

## 🧩 Arquitetura

- Thread 1: Bot do Telegram
- Thread 2: API Flask
- Engine de IA central com suporte a tools externas
- Sistema de execução modular e extensível

---

## 🔧 Tools disponíveis

O sistema suporta tools plugáveis, incluindo:

- Sherlock (OSINT usernames)
- Holehe (emails e serviços associados)
- Outras tools podem ser facilmente adicionadas ao código

---

## 📌 Objetivo

Criar um sistema modular de IA com foco em extensibilidade, permitindo integração rápida de novas ferramentas e fontes de dados.

---

## 🛠️ Tecnologias

- Python
- Flask
- Telegram Bot API
- RAG (Retrieval-Augmented Generation)
- Threads (concurrency)
- OSINT tools

---

## 📎 Status

Projeto em desenvolvimento 🚧

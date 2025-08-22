# LangGraph Chatbot

A production-grade conversational AI application built using **LangGraph** and **Streamlit**, with persistent memory support via **SQLite**. This chatbot allows multi-threaded conversations with the ability to store, retrieve, and delete chat threads efficiently.  

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Tech Stack & Libraries](#tech-stack--libraries)  
- [Detailed Libraries Explanation](#detailed-libraries-explanation)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Project Structure](#project-structure)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Overview

This project integrates **LangGraph**, a stateful conversational graph framework, with **LangChain**’s **ChatOpenAI** interface to create a chatbot that can:  

- Handle multiple chat threads simultaneously.  
- Persist conversation states in **SQLite** for memory.  
- Stream AI responses in real-time using **Streamlit**.  
- Provide a simple, user-friendly web interface for conversations.  

The chatbot uses a **state machine** approach, where every message interaction is a node in a graph, ensuring flexible conversation flows.  

---

## Features

- Multi-threaded conversations  
- Persistent memory using **SQLite**  
- Streamed responses for faster interaction  
- Easy-to-use **Streamlit** UI  
- Thread management: Create, switch, and delete threads  

---

## Tech Stack & Libraries

| Library | Purpose |
|---------|---------|
| **LangGraph** | Provides a state machine-based conversation graph (`StateGraph`) for managing chatbot nodes and edges. Allows persistent memory integration. |
| **LangChain** | Interface for connecting to large language models (LLMs). `ChatOpenAI` is used to communicate with OpenAI-compatible LLMs. |
| **Streamlit** | Frontend framework for building an interactive web UI to chat with the bot. |
| **SQLite3** | Lightweight SQL database used to persist chat thread history and checkpoints. |
| **Pydantic** | Data validation library to define typed dictionaries for chatbot states. |
| **dotenv** | Loads environment variables from a `.env` file to securely store API keys. |
| **UUID** | Generates unique thread IDs for multi-threaded chat sessions. |
| **Typing & Annotated** | Ensures type safety and structured message handling. |

---

## Detailed Libraries Explanation

This section explains each library or module used in the project, its purpose, and why it was chosen:

| Library / Module | Purpose in Project | Notes / Alternatives |
|-----------------|-----------------|-------------------|
| **langgraph.graph** (`StateGraph`, `START`, `END`) | Core of LangGraph’s state machine. `StateGraph` is used to define the nodes (functions) and edges (transitions) in the chatbot conversation flow. `START` and `END` define entry and exit points. | Allows flexible, modular conversation flows compared to linear chat scripts. |
| **typing** (`TypedDict`, `Literal`, `Annotated`) | Used for type hinting and creating structured state dictionaries for the chatbot. `Annotated` allows attaching metadata like the `add_messages` function. | Ensures type safety and code clarity. |
| **langchain_openai / langchain.chat_models / langchain_community.chat_models** (`ChatOpenAI`) | Interface to OpenAI-compatible LLMs. Handles message invocation with the chosen model (`meta-llama/llama-3-8b-instruct`). | Fallback import strategy ensures compatibility with different LangChain versions. |
| **langchain.schema** (`SystemMessage`, `HumanMessage`, `BaseMessage`) | Defines the structure of messages exchanged between user and AI. Distinguishes roles (`user` vs `assistant`). | Provides standardized message objects for LangChain. |
| **dotenv** (`load_dotenv`) | Loads API keys and other secrets from a `.env` file. | Keeps sensitive data out of the source code. |
| **os** | Access environment variables (`OPENAI_API_KEY`, `OPENAI_API_BASE`). | Used in combination with `dotenv` to securely fetch API keys. |
| **pydantic** (`BaseModel`, `Field`) | Provides data validation and type enforcement for complex chatbot states. | Ensures that messages conform to expected structure before passing to LLM. |
| **operator** | Used for functional operations like sorting or comparisons if needed in processing message lists. | Optional but useful for advanced graph operations. |
| **langgraph.graph.message** (`add_messages`) | Utility to handle and append `BaseMessage` objects efficiently in the chatbot state. | Optimized over manually appending messages. |
| **langgraph.checkpoint.sqlite** (`SqliteSaver`) | Implements persistent memory by saving conversation checkpoints to a SQLite database. | Ensures chat threads persist across sessions. |
| **sqlite3** | Standard Python module for database operations. Stores thread and checkpoint information. | Lightweight and suitable for local, production-grade persistence. |
| **streamlit** (`st`) | Frontend framework to build an interactive web interface. Handles user input, message display, and chat threads. | Enables rapid prototyping and deployment of chatbots. |
| **uuid** | Generates unique identifiers for chat threads. Ensures thread separation and avoids collisions. | Essential for multi-threaded conversation management. |

---

## Installation

1. Clone the repository:

git clone https://github.com/yourusername/langgraph-chatbot.git
cd langgraph-chatbot

2. Create a virtual environment:
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Add your environment variables in .env:
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1

```
langgraph-chatbot/
│
├── backend.py          # Chatbot graph, state machine, and database integration
├── app.py              # Streamlit frontend and UI logic
├── requirements.txt    # Python dependencies
├── chatbot.db          # SQLite database for storing conversation states
├── .env                # Environment variables
└── README.md           # Project documentation

# LangGraph Chatbot

A production-grade conversational AI application built using **LangGraph** and **Streamlit**, with persistent memory support via **SQLite** and observability powered by **LangSmith**.  

This chatbot allows multi-threaded conversations with persistent storage, while also tracking conversation metrics such as latency, token usage, and metadata for each thread.  

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

This project integrates:  

- **LangGraph**: for stateful, graph-based conversation flows.  
- **LangChain’s ChatOpenAI**: for LLM interactions with OpenAI-compatible models.  
- **SQLite**: for storing and retrieving multi-threaded conversations.  
- **Streamlit**: for an intuitive chat interface with session management.  
- **LangSmith**: for tracking and monitoring LLM calls with metrics such as latency, token usage, success/failure rates, and metadata.  

The chatbot uses a **state machine** approach, where each interaction is represented as a node in a graph. With **LangSmith integration**, developers also get real-time observability, enabling them to debug and optimize chatbot performance.  

---

## Features

- Multi-threaded conversations  
- Persistent memory using **SQLite**  
- Real-time streamed responses  
- Easy-to-use **Streamlit** UI  
- Thread management: Create, switch, and delete threads  
- **LangSmith Observability**:  
  - Track latency of each LLM call  
  - Monitor token usage (prompt, completion, total)  
  - Add tags & metadata for better debugging  
  - View structured traces of conversation threads  

---

## Tech Stack & Libraries

| Library | Purpose |
|---------|---------|
| **LangGraph** | Conversation graph management with state machine flow. |
| **LangChain** | Provides `ChatOpenAI` to interact with LLMs. |
| **LangSmith** | Observability and monitoring of LLM interactions (latency, token usage, metadata). |
| **Streamlit** | Interactive web interface for chat. |
| **SQLite3** | Persistent storage of conversation history and checkpoints. |
| **Pydantic** | Data validation and typed state management. |
| **dotenv** | Securely load environment variables from `.env`. |
| **UUID** | Generate unique conversation thread IDs. |
| **Typing & Annotated** | Type safety and structured annotations. |

---

## Detailed Libraries Explanation

This section explains each library/module used in the project and why it was chosen:  

| Library / Module | Purpose in Project | Notes / Alternatives |
|------------------|-------------------|----------------------|
| **langgraph.graph** (`StateGraph`, `START`, `END`) | Defines the chatbot’s state machine, with nodes and edges representing conversation flow. | Makes conversation flow modular and flexible. |
| **typing** (`TypedDict`, `Literal`, `Annotated`) | Ensures type safety in defining chatbot states. | Improves clarity and reduces runtime bugs. |
| **langchain_openai / langchain.chat_models / langchain_community.chat_models** (`ChatOpenAI`) | Provides the interface for communicating with OpenAI-compatible LLMs. | Fallback imports for compatibility. |
| **langchain.schema** (`SystemMessage`, `HumanMessage`, `BaseMessage`) | Standard message format for human/AI/system roles. | Provides structure to message history. |
| **dotenv** (`load_dotenv`) | Loads API keys and secrets from `.env`. | Keeps secrets out of codebase. |
| **os** | Accesses environment variables for API keys. | Used alongside `dotenv`. |
| **pydantic** (`BaseModel`, `Field`) | Enforces schema validation for chatbot state. | Guarantees clean data flow. |
| **operator** | Functional utilities (sorting, comparisons, etc.). | Helpful for state operations. |
| **langgraph.graph.message** (`add_messages`) | Optimized helper to append messages in state. | Cleaner than manual appending. |
| **langgraph.checkpoint.sqlite** (`SqliteSaver`) | Saves and retrieves conversation state in SQLite. | Enables memory persistence. |
| **sqlite3** | Core database driver for SQLite. | Lightweight, built-in DB. |
| **streamlit** (`st`) | UI framework for web chat interface. | Easy, Python-first UI. |
| **uuid** | Generates unique conversation thread IDs. | Avoids collisions in session storage. |
| **langsmith** | Tracks all LLM calls: latency, token usage, metadata, and observability features. | Essential for debugging, monitoring, and optimizing LLM apps. |

---

## Installation

1. Clone the repository:

```bash
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
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=langgraph-chatbot


## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py

2. Open the provided local URL (e.g., http://localhost:8501) in your browser.

3. Sidebar options:

New Chat – start a new conversation thread
Switch between previous threads
Delete threads

4. LangSmith Dashboard:

Open LangSmith
View traces for each thread: latency, tokens, and metadata
Debug conversation flow visually

##Project Structure

```bash
langgraph-chatbot/
│
├── backend.py          # Chatbot graph, state machine, and database integration
├── app.py              # Streamlit frontend and UI logic
├── requirements.txt    # Python dependencies
├── chatbot.db          # SQLite database for storing conversation states
├── .env                # Environment variables
└── README.md           # Project documentation

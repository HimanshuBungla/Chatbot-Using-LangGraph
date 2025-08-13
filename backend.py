from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal, Annotated
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, BaseMessage
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
import operator
from langgraph.graph.message import add_messages #more optmized to work with BaseMessages
from langgraph.checkpoint.sqlite import SqliteSaver #Kind of memory in LangGraph that stores things in database
import sqlite3



load_dotenv()

llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE")
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    messages = state['messages']
    
    response = llm.invoke(messages)
    
    return {'messages': [response]}


graph = StateGraph(ChatState)

conn = sqlite3.connect(database='chatbot.db',check_same_thread=False)
checkpointer  = SqliteSaver(conn=conn)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)
    
def delete_thread(thread_id):
    # Ensure UUIDs are converted to string before deletion
    if not isinstance(thread_id, str):
        thread_id = str(thread_id)

    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM checkpoints WHERE thread_id = ?",
        (thread_id,)
    )
    conn.commit()


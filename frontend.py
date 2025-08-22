# import streamlit as st
# from backend import chatbot, retrieve_all_threads
# from langchain_core.messages import HumanMessage
# import uuid

# #*******************************Utility Functions********************************
# def generate_thread_id():
#     """Generate a unique thread ID using UUID."""
#     thread_id = uuid.uuid4()
#     return thread_id

# def reset_chat():
#     st.session_state['message_history'] = []
#     thread_id = generate_thread_id()
#     add_thread(thread_id)
#     st.session_state['thread_id'] = thread_id

# def add_thread(thread_id):
#     if thread_id not in st.session_state['chat_thread']:
#         st.session_state['chat_thread'].append(thread_id)

# def load_conversations(thread_id):
#     """Load conversations from the session state."""
#     return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']

# #********************** Session Setup **********************
# if 'message_history' not in st.session_state:
#     st.session_state['message_history'] = []

# if 'thread_id' not in st.session_state:
#     st.session_state['thread_id'] = generate_thread_id()

# if 'chat_thread' not in st.session_state:
#     st.session_state['chat_thread'] = retrieve_all_threads()

# add_thread(st.session_state['thread_id'])
# #********************** Sidebar UI**********************
# st.sidebar.title("LangGraph Chatbot")
# if st.sidebar.button('New Chat'):
#     reset_chat()
# st.sidebar.header("My Conversations")

# for thread_id in st.session_state['chat_thread'][::-1]:
#     if st.sidebar.button(str(thread_id)):
#         st.session_state['thread_id'] = thread_id
#         messages = load_conversations(thread_id)
#         temp_messages=[]
#         for message in messages:
#             if isinstance(message, HumanMessage):
#                 role = "user"
#             else:
#                 role = "assistant"
#             temp_messages.append({"role": role, "content": message.content})
#         st.session_state['message_history'] = temp_messages


# #********************** Streamlit UI Setup **********************
# for message in st.session_state['message_history']:
#     with st.chat_message(message["role"]):
#             st.text(message["content"])

# user_input = st.chat_input("Type here:", key="input")

# if user_input:

#     # Append user input to message history
#     st.session_state['message_history'].append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.text(user_input)

#     # Stream the response
#     CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
#     response = chatbot.stream(
#         {'messages': [HumanMessage(content=user_input)]}, 
#         config=CONFIG,
#         stream_mode='messages'
#     )
#     with st.chat_message("assistant"):
#         ai_message = st.write_stream(message_chunk.content for message_chunk, metadata in response )
#     st.session_state['message_history'].append({"role": "assistant", "content": ai_message})
#**********************************************************************************
import streamlit as st
from backend import chatbot, retrieve_all_threads, delete_thread
from langchain_core.messages import HumanMessage
import uuid

#*******************************Utility Functions********************************
def generate_thread_id():
    return uuid.uuid4()

def reset_chat():
    st.session_state['message_history'] = []
    thread_id = generate_thread_id()
    add_thread(thread_id)
    st.session_state['thread_id'] = thread_id

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread_id)

def load_conversations(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']

#********************** Session Setup **********************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])

#********************** Sidebar UI**********************
st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header("My Conversations")

for thread_id in st.session_state['chat_thread'][::-1]:
    col1, col2 = st.sidebar.columns([0.8, 0.2])

    with col1:
        if st.button(str(thread_id), key=f"chat_{thread_id}"):
            st.session_state['thread_id'] = thread_id
            messages = load_conversations(thread_id)
            temp_messages = []
            for message in messages:
                role = "user" if isinstance(message, HumanMessage) else "assistant"
                temp_messages.append({"role": role, "content": message.content})
            st.session_state['message_history'] = temp_messages

    with col2:
        if st.button("🗑", key=f"delete_{thread_id}"):
            from backend import delete_thread
            delete_thread(thread_id)  # Remove from DB
            st.session_state['chat_thread'].remove(thread_id)  # Remove from UI
            st.rerun()


#********************** Streamlit UI Setup **********************
for message in st.session_state['message_history']:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type here:", key="input")

if user_input:
    st.session_state['message_history'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    # CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']},
              'metadata': {'thread_id': [st.session_state['thread_id']]},
              'run_name': "git-chat_turn"
    }
    response = chatbot.stream(
        {'messages': [HumanMessage(content=user_input)]}, 
        config=CONFIG,
        stream_mode='messages'
    )
    with st.chat_message("assistant"):
        ai_message = st.write_stream(message_chunk.content for message_chunk, metadata in response)
    st.session_state['message_history'].append({"role": "assistant", "content": ai_message})

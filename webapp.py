import os
import streamlit as st
## faulty error warning here
from llama_index.core import StorageContext, load_index_from_storage
import subprocess

os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]

st.header("Chat with Chip!")

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about IDOT's Specifications!"}
    ]

@st.cache_resource(show_spinner=True)
def load_data():
    with st.spinner(text="Loading IDOT specs... Hang tight - this should only take 1 minute!"):
        PERSIST_DIR = "./storage"
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        vector_index = load_index_from_storage(storage_context)
        return vector_index

index = load_data()
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt + "Preface the answer with the File Name and Page Number.")
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
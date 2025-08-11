# import os
# import json
#
# import streamlit as st
# import openai
#
# #configuring openai - api key
# working_dir = os.path.dirname(os.path.abspath(__file__))
# config_data = json.load(open(f"{working_dir}/config.json"))
# OPENAI_API_KEY = config_data["OPENAI_API_KEY"]
# openai.api_key = OPENAI_API_KEY
#
# #configuring streamlit page settings
# st.set_page_config(
#     page_title='GPT-4o-ChatBot',
#     page_icon='💬',
#     layout="centered"
# )
#
# #initialize chat session in streamlit if not present already
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
#
# #stremalit page title
# st.title("🤖GPT-4o-ChatBot")
#
# #display chat history
# for message in st.session_state.chat_history:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
#
#
# #input field for user message
# user_prompt = st.chat_input("Ask GPT-4o...")
# if user_prompt:
#     # add user's message to chat to display it
#     st.chat_message("user").markdown(user_prompt)
#     st.session_state.chat_history.append({"role":"user", "content":user_prompt})
#
#
#     #send user's message to GPT-4o and get a respinse
#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role":"system","content":"You are a helpful assistant"},
#             *st.session_state.chat_history
#         ]
#     )
#
#     assistant_response = response.choices[0].message.content
#     st.session_state.chat_history.append({"role":"assistant", "content":assistant_response})
#
#
#     #display GPT-4o response
#     with st.chat_message("assistant"):
#         st.markdown(assistant_response)
#



import os
import json
import requests
import streamlit as st
from datetime import datetime

# Load API key from config
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
GROQ_API_KEY = config_data["GROQ_API_KEY"]

# Groq API constants
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
AVAILABLE_MODELS = ["llama3-70b-8192", "mixtral-8x7b-32768"]

# Streamlit config
st.set_page_config(page_title="🤖 GPT Chat with Groq API", page_icon="🧠", layout="centered")

# Sidebar controls
st.sidebar.header("⚙️ Settings")
model = st.sidebar.selectbox("🔍 Choose a Model", AVAILABLE_MODELS)
temperature = st.sidebar.slider("🎛️ Temperature (Creativity)", 0.0, 1.5, 0.7, 0.1)
system_prompt = st.sidebar.text_area("🧪 System Prompt (Optional)", height=100)

# Theme toggle
dark_mode = st.sidebar.toggle("🌓 Dark Mode", value=False)
if dark_mode:
    st.markdown("<style>body { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)

# Clear chat
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

# Download chat
if st.sidebar.button("💾 Download Chat"):
    chat_text = "\n\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.get("chat_history", [])])
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    st.download_button("📥 Save Conversation", chat_text, f"chat_{timestamp}.txt", mime="text/plain")

# Header
st.markdown("<h1 style='text-align: center;'>🤖 GPT Chat with Groq API</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Built with ❤️ using Streamlit + Groq API</p>", unsafe_allow_html=True)
st.divider()

# Chat history init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    if system_prompt.strip():
        st.session_state.chat_history.append({"role": "system", "content": system_prompt})
    st.session_state.chat_history.append({"role": "assistant", "content": "👋 Hello! I'm GroqGPT. How can I help you today?"})

# Display chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_prompt = st.chat_input("Type your message here... 💬")

if user_prompt:
    # Show user message
    st.chat_message("user").markdown(f"🧑‍💻 {user_prompt}")
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # API call setup
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": st.session_state.chat_history,
        "temperature": temperature
    }

    # Make request
    with st.spinner("⚡ Thinking..."):
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        st.session_state.chat_history.append({"role": "assistant", "content": f"🤖 {reply}"})
        with st.chat_message("assistant"):
            st.markdown(f"🤖 {reply}")
    else:
        st.error(f"❌ API Error {response.status_code}: {response.text}")
# kuch nhi bhai bss streak banane ke liye bakch*di kr rha

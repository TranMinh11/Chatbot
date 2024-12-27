import streamlit as st
from chatbot import get_chatbot_response

st.title("Dynamic Personality Chatbot")
st.write("Chat with dynamic characters")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

character = st.radio("Choose a character to chat with:", ("Linh", "Mai", "Hạ"))

with st.chat_message("assistant"):
    st.markdown(f"Dynamic Personality Chatbot ({character}) is ready to chat with you.")

user_input = st.chat_input("Type your message here...")

if user_input:
    response = get_chatbot_response(user_input, character)

    st.session_state.chat_history.append({"user": user_input, "bot": response})

    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(chat["user"])
        with st.chat_message("assistant"):
            st.markdown(chat["bot"])
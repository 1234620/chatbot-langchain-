import streamlit as st
import requests

st.set_page_config(page_title="Travel Chatbot", page_icon="✈️")

st.title("✈️ Travel Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input field pinned to the bottom
if user_input := st.chat_input("Ask me anything about your travel plans..."):
    # Append user input to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call your backend
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"message": user_input},
            timeout=15
        )
        bot_reply = response.json().get("response", "Sorry, I couldn't understand that.")
    except Exception as e:
        bot_reply = f"❌ Error: {str(e)}"

    # Append bot reply to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Display bot reply
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
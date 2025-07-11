import streamlit as st
import chatbot_backend as demo  # Import your chatbot backend

# --- Custom CSS ---
st.markdown("""
    <style>
        .main {
            background-color: #1e1e1e;
        }
        body {
            background-color: #1e1e1e;
            color: white;
        }
        .stApp {
            background-color: #1e1e1e;
        }
    </style>
""", unsafe_allow_html=True)


# --- Sidebar ---
with st.sidebar:
    st.image("https://ui-avatars.com/api/?name=Ahmed&background=0D8ABC&color=fff&size=128", width=80)
    st.markdown("## Hello, Ahmed ")
    st.markdown("Welcome to your chatbot. Start a conversation below!")

# --- Title and Description ---
st.markdown("<h1 style='text-align: center; color: #0d8abc;'> Memory Based Chatbot </h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Powered by Streamlit & AWS</p>", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'memory' not in st.session_state:
    st.session_state.memory = demo.demo_memory()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- Chat History Display ---
import html  # Add this import at the top of your script

# --- Display Chat History ---
for message in st.session_state.chat_history:
    role = message["role"]
    escaped_text = html.escape(message["text"])  # Prevents </div> from being misread

    if role == "user":
        avatar_url = "https://cdn-icons-png.flaticon.com/512/12963/12963337.png"  # Human
        align = "right"
        bubble_bg = "#2c2c2c"
        text_color = "#ffffff"
        avatar_pos = "margin-left: 10px;"
        msg_margin = "margin-left: auto; margin-right: 0;"
    else:
        avatar_url = "https://cdn-icons-png.flaticon.com/512/4712/4712109.png"  # AI
        align = "left"
        bubble_bg = "#ffffff"
        text_color = "#222222"
        avatar_pos = "margin-right: 10px;"
        msg_margin = "margin-right: auto; margin-left: 0;"

    st.markdown(f"""
    <div style="display: flex; justify-content: {align}; align-items: flex-start; margin-bottom: 1em;">
        <img src="{avatar_url}" style="width: 32px; height: 32px; border-radius: 50%; {avatar_pos}">
        <div style="background: {bubble_bg}; color: {text_color}; padding: 0.8em 1em;
                    border-radius: 1em; max-width: 70%; {msg_margin}; font-size: 1.05em;
                    border: 1px solid #ccc; line-height: 1.4; white-space: pre-wrap;">
            {escaped_text}
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- Chat Input Box ---
input_text = st.chat_input("Type your message here...")

if input_text:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "text": input_text})

    # Get bot response with spinner
    with st.spinner("Thinking..."):
        response = demo.demo_conversation(
            input_text=input_text,
            memory=st.session_state.memory
        )

    # Add bot response
    st.session_state.chat_history.append({"role": "assistant", "text": response})
    
    # Rerun to refresh and display the new messages
    st.rerun()

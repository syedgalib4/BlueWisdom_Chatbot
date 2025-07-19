# app.py (Blue Wisdom AI Chatbot for Gemini API)

import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
import os

# --- 1. UI CONFIGURATION & STYLING ---

st.set_page_config(page_title="Blue Wisdom", layout="wide", initial_sidebar_state="auto")

def load_css():
    """Injects custom CSS for a professional, modern UI."""
    st.markdown("""
        <style>
            /* Import Google Font */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

            /* General Body Styles */
            html, body, [class*="st-"] {
                font-family: 'Inter', sans-serif;
            }

            /* Main container for the app - Sky Ocean Blue Gradient */
            .stApp {
                background-image: linear-gradient(180deg, #E0F7FA, #FFFFFF);
                color: #1E1E1E; /* Dark text for light background */
            }

            /* Hide Streamlit's default footer and header */
            footer, [data-testid="stHeader"] {
                visibility: hidden;
            }
            
            /* Centered Title */
            h1 {
                text-align: center;
                color: #004D40; /* Dark teal for title */
                font-weight: 700;
            }
            
            p[data-testid="stCaption"] {
                text-align: center;
                color: #00796B; /* Teal for caption */
            }

            /* Sidebar styling */
            [data-testid="stSidebar"] {
                background-color: #FFFFFF;
                border-right: 1px solid #B2DFDB;
            }
            
            .stButton>button {
                width: 100%;
                border-radius: 0.5rem;
                color: #004D40;
                background-color: #E0F2F1;
                border: 1px solid #B2DFDB;
                transition: all 0.2s ease-in-out;
            }
            .stButton>button:hover {
                background-color: #B2DFDB;
                border-color: #80CBC4;
                color: #004D40;
            }
            
            /* Chat message styling */
            .chat-message {
                padding: 1rem 1.25rem;
                border-radius: 1.25rem;
                margin-bottom: 1rem;
                box-shadow: 0 4px 20px 0 rgba(0,0,0,0.08);
                display: flex;
                align-items: flex-start;
                gap: 15px;
                max-width: 80%;
                opacity: 0;
                animation: slideIn 0.4s ease-out forwards;
                border: 1px solid #E0E0E0;
            }

            @keyframes slideIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .chat-avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                flex-shrink: 0;
            }
            
            .message-content {
                padding-top: 5px;
            }

            /* User message container */
            .user-message-container {
                display: flex;
                justify-content: flex-end;
            }
            .user-message {
                background-color: #007BFF;
                color: #FFFFFF;
                border-top-right-radius: 0.5rem;
            }
            .user-avatar {
                background-color: #0056b3;
                color: #FFFFFF;
            }

            /* Assistant message container */
            .assistant-message-container {
                display: flex;
                justify-content: flex-start;
            }
            .assistant-message {
                background-color: #F8F9FA;
                color: #212529;
                border-top-left-radius: 0.5rem;
            }
            .assistant-avatar {
                background-color: #E9ECEF;
                color: #495057;
            }

            /* API Key input styling */
            div[data-testid="stTextInput"] input {
                background-color: #FFFFFF;
                color: #212529;
                border: 1px solid #B2DFDB;
                border-radius: 0.5rem;
            }
            
            /* Chat input bar styling */
            div[data-testid="stChatInput"] {
                background-color: transparent;
            }
            
            /* Spinner (AI is thinking...) styling */
            .stSpinner > div {
                border-top-color: #007BFF !important;
                border-right-color: #007BFF !important;
            }
        </style>
    """, unsafe_allow_html=True)

# Load the custom CSS
load_css()

# --- 2. INITIALIZATION & CONFIGURATION ---

def get_voice_components():
    if 'recognizer' not in st.session_state:
        try:
            st.session_state.recognizer = sr.Recognizer()
        except Exception as e:
            st.error(f"Error initializing Speech Recognizer: {e}")
            st.session_state.recognizer = None
    return st.session_state.get('recognizer')

# --- SESSION STATE MANAGEMENT FOR MULTI-CHAT ---
if 'api_key' not in st.session_state:
    st.session_state.api_key = None
if 'all_chats' not in st.session_state:
    st.session_state.all_chats = []
if 'active_chat_index' not in st.session_state:
    st.session_state.active_chat_index = -1

# --- GEMINI API SETUP ---
if not st.session_state.api_key:
    api_key_input = st.text_input("Enter your Google Gemini API Key:", type="password", key="api_key_input_widget")
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.rerun()
else:
    if not st.session_state.all_chats:
        try:
            genai.configure(api_key=st.session_state.api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            first_chat_session = {
                'history': [],
                'gemini_chat': model.start_chat(history=[])
            }
            st.session_state.all_chats.append(first_chat_session)
            st.session_state.active_chat_index = 0
            if 'model_initialized' not in st.session_state:
                st.success("Gemini model initialized successfully!")
                st.session_state.model_initialized = True
        except Exception as e:
            st.error(f"Failed to configure Gemini: {e}. Please check your API key and try again.")
            st.session_state.api_key = None

# --- 4. UI LAYOUT ---

def new_chat():
    """Starts a new chat session."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        new_chat_session = {
            'history': [],
            'gemini_chat': model.start_chat(history=[])
        }
        st.session_state.all_chats.append(new_chat_session)
        st.session_state.active_chat_index = len(st.session_state.all_chats) - 1
        st.rerun()
    except Exception as e:
        st.error(f"Could not start a new chat: {e}")

# Sidebar for Chat History
with st.sidebar:
    st.title("Chats")
    if st.button("➕ New Chat", use_container_width=True, disabled=(not st.session_state.api_key)):
        new_chat()
    
    st.markdown("---")
    
    if not st.session_state.all_chats:
        st.info("Your conversations will appear here.")
    else:
        for i, chat_session in enumerate(st.session_state.all_chats):
            chat_title = "New Chat"
            if chat_session['history']:
                for msg in chat_session['history']:
                    if msg['role'] == 'user':
                        chat_title = msg['content']
                        break
            
            if len(chat_title) > 30:
                chat_title = chat_title[:27] + "..."
            
            if st.button(f"💬 {chat_title}", key=f"chat_{i}", use_container_width=True):
                 st.session_state.active_chat_index = i
                 st.rerun()

# Main chat interface
st.markdown("<h1 style='text-align: center;'>Blue Wisdom</h1>", unsafe_allow_html=True)
st.caption("Powered by Google Gemini")

active_chat_history = []
if st.session_state.active_chat_index != -1 and st.session_state.all_chats:
    active_chat_history = st.session_state.all_chats[st.session_state.active_chat_index]['history']

if not active_chat_history and st.session_state.api_key:
    st.info("Welcome to Blue Wisdom! How can I help you today?")

chat_container = st.container()
with chat_container:
    for message in active_chat_history:
        is_user = message["role"] == "user"
        avatar_emoji = "🧑‍🎓" if is_user else "🧘"
        container_class = "user-message-container" if is_user else "assistant-message-container"
        message_class = "chat-message user-message" if is_user else "chat-message assistant-message"
        avatar_class = "chat-avatar user-avatar" if is_user else "chat-avatar assistant-avatar"
        
        st.markdown(f"""
            <div class="{container_class}">
                <div class="{message_class}">
                    <div class="{avatar_class}">{avatar_emoji}</div>
                    <div class="message-content">{message['content']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 5. CORE CHATBOT FUNCTION ---
def generate_response(user_input):
    active_index = st.session_state.active_chat_index
    if active_index == -1:
        return
    
    active_chat_session = st.session_state.all_chats[active_index]
    active_chat_session['history'].append({"role": "user", "content": user_input})
    
    try:
        response = active_chat_session['gemini_chat'].send_message(user_input)
        ai_response = response.text
    except Exception as e:
        ai_response = f"An error occurred: {e}"
        st.error(ai_response)

    active_chat_session['history'].append({"role": "assistant", "content": ai_response})

# --- 6. USER INPUT HANDLERS ---
is_model_ready = st.session_state.active_chat_index != -1

if prompt := st.chat_input("Ask Blue Wisdom...", disabled=not is_model_ready):
    with st.spinner("Blue Wisdom is thinking..."):
        generate_response(prompt)
    st.rerun()

if st.button("Ask with Voice 🎙️", use_container_width=True, disabled=not is_model_ready):
    with st.spinner("Listening..."):
        r = get_voice_components()
        if r:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)
                    spoken_prompt = r.recognize_google(audio, language='en-in')
                    with st.spinner("Blue Wisdom is thinking..."):
                        generate_response(spoken_prompt)
                    st.rerun()
                except Exception as e:
                    st.warning(f"Could not process voice input: {e}")
        else:
            st.error("Speech recognizer not available.")

# config.py
import os

try:
    import streamlit as st
    STREAMLIT = True
except:
    STREAMLIT = False

def get_secret(key):
    # Pehle Streamlit secrets try karo
    if STREAMLIT:
        try:
            val = st.secrets.get(key)
            if val:
                return val
        except:
            pass
    # Phir .env try karo
    return os.getenv(key)

# Groq API
GROQ_API_KEY = get_secret("GROQ_API_KEY")

# Email Credentials
EMAIL_ADDRESS = get_secret("EMAIL_ADDRESS")
EMAIL_PASSWORD = get_secret("EMAIL_PASSWORD")

# IMAP / SMTP Settings
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT   = 993
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587

# LLM Model
MODEL_NAME = "llama-3.1-8b-instant"

# Database
DB_PATH = "sales_agent.db"

# FAISS
FAISS_INDEX_PATH = "faiss_index"
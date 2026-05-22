# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Email Credentials
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

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
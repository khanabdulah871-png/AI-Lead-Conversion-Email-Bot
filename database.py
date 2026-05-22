# database.py
import sqlite3
import config

def get_connection():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Leads table — har customer ka record
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            sender      TEXT NOT NULL,
            subject     TEXT,
            body        TEXT,
            intent      TEXT,
            lead_score  INTEGER,
            status      TEXT DEFAULT 'pending',
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Conversations table — email history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id     INTEGER,
            role        TEXT,
            message     TEXT,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tables ban gayi hain!")

def save_lead(sender, subject, body, intent, lead_score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leads (sender, subject, body, intent, lead_score)
        VALUES (?, ?, ?, ?, ?)
    """, (sender, subject, body, intent, lead_score))
    conn.commit()
    lead_id = cursor.lastrowid
    conn.close()
    return lead_id

def save_message(lead_id, role, message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversations (lead_id, role, message)
        VALUES (?, ?, ?)
    """, (lead_id, role, message))
    conn.commit()
    conn.close()

def get_all_leads():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads ORDER BY created_at DESC")
    leads = cursor.fetchall()
    conn.close()
    return leads

def get_conversation(lead_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM conversations 
        WHERE lead_id = ? 
        ORDER BY created_at ASC
    """, (lead_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

def update_lead_status(lead_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE leads SET status = ? WHERE id = ?
    """, (status, lead_id))
    conn.commit()
    conn.close()
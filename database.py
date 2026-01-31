import sqlite3
from datetime import datetime

conn = sqlite3.connect("support.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS cases (
    case_id TEXT PRIMARY KEY,
    user_id INTEGER,
    user_name TEXT,
    user_uid TEXT,
    user_email TEXT,
    problem TEXT,
    status TEXT,
    assigned_agent INTEGER,
    created_at TEXT,
    updated_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id TEXT,
    sender TEXT,
    sender_name TEXT,
    message_type TEXT,
    content TEXT,
    timestamp TEXT
)
""")
conn.commit()

# Functions
def create_case(user_id, name, uid, email, problem):
    from config import CASE_COUNTER
    CASE_COUNTER += 1
    case_id = f"BF-{datetime.now().year}-{CASE_COUNTER:06}"
    cursor.execute("""
        INSERT INTO cases (case_id, user_id, user_name, user_uid, user_email, problem, status, assigned_agent, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (case_id, user_id, name, uid, email, problem, "OPEN", None, datetime.now(), datetime.now()))
    conn.commit()
    return case_id

def add_message(case_id, sender, sender_name, msg_type, content):
    cursor.execute("""
        INSERT INTO messages (case_id, sender, sender_name, message_type, content, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (case_id, sender, sender_name, msg_type, content, datetime.now()))
    conn.commit()

def get_case(case_id):
    cursor.execute("SELECT * FROM cases WHERE case_id=?", (case_id,))
    return cursor.fetchone()

def get_user_open_case(user_id):
    cursor.execute("SELECT * FROM cases WHERE user_id=? AND status IN ('OPEN', 'IN_PROGRESS')", (user_id,))
    return cursor.fetchone()

def assign_agent(case_id, agent_id):
    cursor.execute("UPDATE cases SET assigned_agent=?, status='IN_PROGRESS', updated_at=? WHERE case_id=?", 
                   (agent_id, datetime.now(), case_id))
    conn.commit()

def close_case(case_id):
    cursor.execute("UPDATE cases SET status='CLOSED', updated_at=? WHERE case_id=?", (datetime.now(), case_id))
    conn.commit()

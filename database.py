# # import sqlite3

# # def init_db():
# #     conn = sqlite3.connect("resolveiq.db")
# #     c = conn.cursor()

# #     c.execute("""
# #     CREATE TABLE IF NOT EXISTS tickets (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         timestamp TEXT,
# #         ticket TEXT,
# #         category TEXT,
# #         priority TEXT,
# #         sentiment TEXT,
# #         confidence INTEGER,
# #         resolution TEXT
# #     )
# #     """)

# #     conn.commit()
# #     conn.close()

# # def insert_ticket(data):
# #     conn = sqlite3.connect("resolveiq.db")
# #     c = conn.cursor()

# #     c.execute("""
# #     INSERT INTO tickets (timestamp, ticket, category, priority, sentiment, confidence, resolution)
# #     VALUES (?, ?, ?, ?, ?, ?, ?)
# #     """, (
# #         data["timestamp"],
# #         data["original_ticket"],
# #         data["category"],
# #         data["priority"],
# #         data["sentiment"],
# #         data["confidence_score"],
# #         data["resolution"]
# #     ))

# #     conn.commit()
# #     conn.close()

# # def get_all_tickets():
# #     conn = sqlite3.connect("resolveiq.db")
# #     c = conn.cursor()

# #     c.execute("SELECT * FROM tickets")
# #     rows = c.fetchall()

# #     conn.close()
# #     return rows
# import sqlite3
# import hashlib

# # Connect to SQLite DB
# def connect_db():
#     return sqlite3.connect("tickets.db", check_same_thread=False)

# conn = connect_db()
# cursor = conn.cursor()

# # Create user table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT UNIQUE,
#     password TEXT
# )
# """)
# conn.commit()


# # Hash password
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()


# # Add user
# def add_user(username, password):
#     try:
#         hashed_pw = hash_password(password)
#         cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
#         conn.commit()
#         return True
#     except:
#         return False


# # Authenticate user
# def authenticate(username, password):
#     hashed_pw = hash_password(password)
#     cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pw))
#     return cursor.fetchone()

import sqlite3
import json
DB_NAME = "tickets.db"
conn = sqlite3.connect("tickets.db", check_same_thread=False)
cursor = conn.cursor()

def get_connection():
    return sqlite3.connect(DB_NAME)

# Create user table
def create_user_table():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    
    conn.commit()
    conn.close()


# Add new user
def add_user(username, password):
    conn = get_connection()
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except:
        pass
    
    conn.close()


# Authenticate user
def authenticate(username, password):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()

    conn.close()

    return user

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    category TEXT,
    priority TEXT,
    sentiment TEXT,
    confidence INTEGER,
    summary TEXT,
    resolution TEXT,
    customer_reply TEXT,
    assigned_team TEXT,
    original_ticket TEXT
)
""")

conn.commit()


def save_ticket(ticket):
    cursor.execute("""
    INSERT INTO tickets (
        timestamp, category, priority, sentiment, confidence,
        summary, resolution, customer_reply, assigned_team, original_ticket
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket["timestamp"],
        ticket["category"],
        ticket["priority"],
        ticket["sentiment"],
        ticket["confidence_score"],
        ticket["summary"],
        ticket["resolution"],
        ticket["customer_reply"],
        ticket["assigned_team"],
        ticket["original_ticket"]
    ))

    conn.commit()


def get_tickets():
    cursor.execute("SELECT * FROM tickets ORDER BY id DESC")

    rows = cursor.fetchall()

    tickets = []

    for r in rows:
        tickets.append({
            "timestamp": r[1],
            "category": r[2],
            "priority": r[3],
            "sentiment": r[4],
            "confidence_score": r[5],
            "summary": r[6],
            "resolution": r[7],
            "customer_reply": r[8],
            "assigned_team": r[9],
            "original_ticket": r[10]
        })

    return tickets
import sqlite3


def get_connection(db_path="memory.db"):
    return sqlite3.connect(db_path, check_same_thread=False)


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT
            role TEXT,
            content TEXT
        )
    """)
    conn.commit()
from ai_companion.core.db import get_connection, init_db


class SessionMemory:
    def __init__(self):
        self.conn = get_connection()
        init_db(self.conn)

    def add_message(self, user_id, role, content):
        self.conn.execute(
            "INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)",
            (user_id, role, content)
        )
        self.conn.commit()

    def get_recent_messages(self, user_id, limit: int = 10):
        cursor = self.conn.execute(
            "SELECT role, content FROM messages WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit)
        )

        rows = cursor.fetchall()
        rows.reverse()

        return [{"role": r, "content": c} for r, c in rows]

    def clear(self):
        self.conn.execute("DELETE FROM messages")
        self.conn.commit()



session_memory_instance = None


def get_session_memory():
    global session_memory_instance

    if session_memory_instance is None:
        session_memory_instance = SessionMemory()

    return session_memory_instance
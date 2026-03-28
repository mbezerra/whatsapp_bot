"""
Módulo para gerenciamento do histórico de conversas em um banco de dados SQLite.
"""
import sqlite3
import os

class ChatHistoryDB:
    """
    Gerenciador de persistência do histórico de conversas utilizando SQLite.
    """
    def __init__(self, db_path: str = "data/chat_history.db"):
        """
        Inicializa o gerenciador de banco de dados.
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """
        Cria a estrutura de pastas e a tabela de mensagens se não existirem.
        """
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def add_message(self, session_id: str, role: str, content: str):
        """
        Adiciona uma nova mensagem ao histórico de uma sessão.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
                (session_id, role, content)
            )

    def get_history(self, session_id: str, limit: int = 10):
        """
        Recupera as últimas mensagens de uma sessão, ordenadas cronologicamente.
        """
        with sqlite3.connect(self.db_path) as conn:
            query = """
                SELECT role, content FROM messages
                WHERE session_id = ?
                ORDER BY timestamp DESC LIMIT ?
            """
            cursor = conn.execute(query, (session_id, limit))
            rows = cursor.fetchall()
            # Retorna do mais antigo para o mais recente
            return rows[::-1]

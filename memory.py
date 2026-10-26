import sqlite3
from pathlib import Path
from datetime import datetime


# Store the database beside this Python file.
MEMORY_DB = Path(__file__).parent / "samaritan_memory.db"

def get_connection():
    """Open a connection to Samaritan's SQLite database."""
    connection = sqlite3.connect(MEMORY_DB)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_memory():
    """Create the memories table if it does not exist."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()


def save_memory(content):
    """Save one memory to the database."""
    content = content.strip()
    if not content:
        return {
            "success": False,
            "error": "Memory cannot be empty."
        }
    connection = get_connection()
    cursor = connection.cursor()
    created_at = datetime.now().isoformat(
        timespec="seconds"
    )
    cursor.execute(
        """
        INSERT INTO memories (content, created_at)
        VALUES (?, ?)
        """,
        (content, created_at)
    )
    memory_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return {
        "success": True,
        "id": memory_id,
        "content": content,
        "created_at": created_at
    }


def get_all_memories():
    """Return all saved memories in ID order."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, content, created_at
        FROM memories
        ORDER BY id ASC
        """
    )
    memories = [
        dict(row)
        for row in cursor.fetchall()
    ]
    connection.close()
    return memories


def search_memories(query):
    """Find memories containing the requested text."""
    query = query.strip()
    if not query:
        return []
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, content, created_at
        FROM memories
        WHERE content LIKE ?
        ORDER BY id ASC
        """,
        (f"%{query}%",)
    )
    memories = [
        dict(row)
        for row in cursor.fetchall()
    ]
    connection.close()
    return memories


def delete_memory(memory_id):
    """Delete one memory using its database ID."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        DELETE FROM memories
        WHERE id = ?
        """,
        (memory_id,)
    )
    deleted = cursor.rowcount > 0
    connection.commit()
    connection.close()
    return deleted


def clear_memories():
    """Delete every saved memory."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM memories")
    deleted_count = cursor.rowcount
    connection.commit()
    connection.close()
    return deleted_count

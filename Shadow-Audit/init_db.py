import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "mock_production.db"

def init_database(db_path: Path = DB_PATH):
    """Initialize the SQLite database with system_configs and audit_tasks tables."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Create configuration tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_configs (
                variable_name TEXT PRIMARY KEY,
                current_value INTEGER
            )
        ''')
        cursor.execute('''
            INSERT OR IGNORE INTO system_configs (variable_name, current_value)
            VALUES ('MIN_KEY_LENGTH', 1024)
        ''')
        
        # Create task tracking table to store the "LOCKED" state
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_tasks (
                task_id TEXT PRIMARY KEY,
                status TEXT
            )
        ''')
    print("Database initialized successfully with system_configs and audit_tasks tables.")

if __name__ == "__main__":
    init_database()
import sqlite3

def start_db():
        return sqlite3.connect('app/tasks.db')


def get_db():
    conn = start_db()
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    cursor.close()
    conn.row_factory = sqlite3.Row  
    try:
        yield conn
    finally:
        conn.close()

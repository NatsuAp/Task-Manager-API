import sqlite3

def start_db_sqlite():
        return sqlite3.connect('app/tasks.db')


def get_db_sqlite   ():
    conn = start_db_sqlite()
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    cursor.close()
    conn.row_factory = sqlite3.Row  
    try:
        yield conn
    finally:
        conn.close()

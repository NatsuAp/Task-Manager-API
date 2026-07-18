import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor
from rich.table import Row


def start_db_postgresql():
    return psycopg2.connect("dbname=task_manager user=andres", cursor_factory=DictCursor)

def get_db_postgresql():
    conn = start_db_postgresql()
    try:
        yield conn
    finally:
        conn.close()


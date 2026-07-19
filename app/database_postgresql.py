import psycopg2
import os
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

def start_db_postgresql():
    load_dotenv()
    params = "dbname=task_manager user=andres password=" + os.getenv("password")
    return psycopg2.connect(params, cursor_factory=DictCursor)

def get_db_postgresql():
    conn = start_db_postgresql()
    try:
        yield conn
    finally:
        conn.close()


import psycopg2
from 
def start_db():
    conn = psycopg2.connect("dbname=task_manager user=andres password= ")
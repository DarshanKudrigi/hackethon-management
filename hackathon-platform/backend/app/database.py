import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
import os

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "9876"),
    "database": os.getenv("DB_NAME", "hackathon_db"),
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="hackathon_pool",
    pool_size=5,
    **db_config
)

def get_db():
    connection = connection_pool.get_connection()
    try:
        yield connection
    finally:
        connection.close()

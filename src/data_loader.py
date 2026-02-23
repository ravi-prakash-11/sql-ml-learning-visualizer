import sqlite3
import pandas as pd

DB_PATH = "data/database.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def fetch_dataframe(query: str) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    print(fetch_dataframe(query))
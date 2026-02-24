#1st data loader
# import sqlite3
# import pandas as pd

# DB_PATH = "data/database.db"

# def get_connection():
#     return sqlite3.connect(DB_PATH)

# def fetch_dataframe(query: str) -> pd.DataFrame:
#     conn = get_connection()
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df

# if __name__ == "__main__":
#     query = "SELECT name FROM sqlite_master WHERE type='table';"
#     print(fetch_dataframe(query))
#
#--------------------------------------------------------------------------

#2nd data load
import sqlite3
import random
from datetime import datetime, timedelta
import pandas as pd

DB_PATH = "data/database.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_customers(n=500):
    customers = []
    for i in range(1, n + 1):
        customers.append((
            i,
            random.randint(18, 65),
            random.choice(["Male", "Female"]),
            random.choice(["US", "EU", "Asia"])
        ))
    return customers


def create_transactions(customers, min_txn=3, max_txn=10):
    transactions = []
    txn_id = 1
    for customer_id, *_ in customers:
        for _ in range(random.randint(min_txn, max_txn)):
            transactions.append((
                txn_id,
                customer_id,
                round(random.uniform(10, 300), 2),
                random.choice(["Electronics", "Clothing", "Food", "Books"]),
                (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
            ))
            txn_id += 1
    return transactions


def create_sessions(customers):
    sessions = []
    session_id = 1
    for customer_id, *_ in customers:
        for _ in range(random.randint(1, 5)):
            sessions.append((
                session_id,
                customer_id,
                round(random.uniform(1, 30), 2),
                random.randint(1, 20)
            ))
            session_id += 1
    return sessions


# def insert_data():
#     conn = get_connection()
#     cursor = conn.cursor()

#     customers = create_customers()
#     transactions = create_transactions(customers)
#     sessions = create_sessions(customers)

#     cursor.executemany(
#         "INSERT INTO customers VALUES (?, ?, ?, ?)", customers
#     )
#     cursor.executemany(
#         "INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", transactions
#     )
#     cursor.executemany(
#         "INSERT INTO sessions VALUES (?, ?, ?, ?)", sessions
#     )

#     conn.commit()
#     conn.close()

#     print("✅ Synthetic data inserted successfully!")

def insert_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing data to avoid duplicates
    cursor.execute("DELETE FROM sessions;")
    cursor.execute("DELETE FROM transactions;")
    cursor.execute("DELETE FROM customers;")

    customers = create_customers()
    transactions = create_transactions(customers)
    sessions = create_sessions(customers)

    cursor.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?)", customers
    )
    cursor.executemany(
        "INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", transactions
    )
    cursor.executemany(
        "INSERT INTO sessions VALUES (?, ?, ?, ?)", sessions
    )

    conn.commit()
    conn.close()

    print("Synthetic data refreshed successfully!")

if __name__ == "__main__":
    insert_data()
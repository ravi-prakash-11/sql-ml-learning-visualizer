-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    location TEXT
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount REAL,
    category TEXT,
    timestamp TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Sessions table
CREATE TABLE IF NOT EXISTS sessions (
    session_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    duration REAL,
    pages_viewed INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
## Create SQLite database for stocks and reddit mentions

import sqlite3

connection = sqlite3.connect()

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY,
        symbol TEXT NOT NULL,
        name TEXT NOT NULL,
        exchange TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS mention (
        stock_id INTEGER,
        stock_symb TEXT NOT NULL,
        dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        message TEXT NOT NULL,
        source TEXT NOT NULL,
        url TEXT NOT NULL,
        PRIMARY KEY (stock_id, dt),
        CONSTRAINT fk_mention_stock FOREIGN KEY (stock_id) REFERENCES stock (id)
    )

""")

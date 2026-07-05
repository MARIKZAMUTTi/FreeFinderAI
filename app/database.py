import sqlite3

DB_PATH = "freefinder.db"


def connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        city TEXT,
        budget INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def add_user(telegram_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO users (telegram_id)
    VALUES (?)
    """, (telegram_id,))

    conn.commit()
    conn.close()


def set_city(telegram_id, city):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE users SET city = ?
    WHERE telegram_id = ?
    """, (city, telegram_id))

    conn.commit()
    conn.close()


def get_user(telegram_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT telegram_id, city, budget
    FROM users
    WHERE telegram_id = ?
    """, (telegram_id,))

    result = cur.fetchone()
    conn.close()

    return result

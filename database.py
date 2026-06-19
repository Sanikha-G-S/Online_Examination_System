import sqlite3

DB_NAME = "exam.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB,
        role TEXT DEFAULT 'student'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exams(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exam_name TEXT,
        duration INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exam_id INTEGER,
        question TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        answer TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        exam_id INTEGER,
        score INTEGER,
        total INTEGER
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database Ready")
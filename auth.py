import sqlite3
import bcrypt

DB_NAME = "exam.db"


def register_user(username, password, role="student"):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:

        cursor.execute(
            """
            INSERT INTO users(username,password,role)
            VALUES(?,?,?)
            """,
            (username, hashed, role)
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def login_user(username, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,username,password,role
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        if bcrypt.checkpw(
            password.encode(),
            user[2]
        ):

            return {
                "id": user[0],
                "username": user[1],
                "role": user[3]
            }

    return None
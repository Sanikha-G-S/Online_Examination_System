import sqlite3
import bcrypt

DB_NAME = "exam.db"

def register_user(username, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:
        cursor.execute(
            """
            INSERT INTO users(username,password)
            VALUES(?,?)
            """,
            (username, hashed_password)
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
        SELECT id, username, password, role
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        user_id = user[0]
        uname = user[1]
        stored_password = user[2]
        role = user[3]

        if bcrypt.checkpw(
            password.encode(),
            stored_password
        ):
            return {
                "id": user_id,
                "username": uname,
                "role": role
            }

    return None
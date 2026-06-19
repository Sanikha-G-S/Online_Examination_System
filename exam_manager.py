import sqlite3

DB_NAME = "exam.db"


def create_exam(exam_name, duration):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO exams(exam_name,duration)
        VALUES(?,?)
        """,
        (exam_name, duration)
    )

    conn.commit()
    conn.close()


def get_all_exams():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,exam_name,duration
        FROM exams
        """
    )

    exams = cursor.fetchall()

    conn.close()

    return exams
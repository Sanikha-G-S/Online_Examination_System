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


def add_question(
        exam_id,
        question,
        option1,
        option2,
        option3,
        option4,
        answer):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO questions(
        exam_id,
        question,
        option1,
        option2,
        option3,
        option4,
        answer
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            exam_id,
            question,
            option1,
            option2,
            option3,
            option4,
            answer
        )
    )

    conn.commit()
    conn.close()


def get_questions(exam_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM questions
        WHERE exam_id=?
        """,
        (exam_id,)
    )

    data = cursor.fetchall()

    conn.close()

    return data


def save_result(
        username,
        exam_id,
        score,
        total):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO results(
        username,
        exam_id,
        score,
        total
        )
        VALUES(?,?,?,?)
        """,
        (
            username,
            exam_id,
            score,
            total
        )
    )

    conn.commit()
    conn.close()


def get_results(username):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM results
        WHERE username=?
        """,
        (username,)
    )

    data = cursor.fetchall()

    conn.close()

    return data
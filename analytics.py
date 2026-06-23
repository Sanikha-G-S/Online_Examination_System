import sqlite3
import pandas as pd

DB_NAME = "exam.db"


def get_statistics():

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM results",
        conn
    )

    conn.close()

    if len(df) == 0:

        return {
            "students": 0,
            "average": 0,
            "highest": 0,
            "lowest": 0
        }

    percentages = (
        df["score"] / df["total"]
    ) * 100

    return {
        "students": len(df),
        "average": round(percentages.mean(), 2),
        "highest": round(percentages.max(), 2),
        "lowest": round(percentages.min(), 2)
    }


def get_leaderboard():

    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT
        username,
        score,
        total
    FROM results
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    if len(df) == 0:
        return pd.DataFrame()

    df["percentage"] = (
        df["score"] / df["total"]
    ) * 100

    df = df.sort_values(
        by="percentage",
        ascending=False
    )

    return df
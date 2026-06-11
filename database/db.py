import sqlite3
from datetime import datetime


class DatabaseManager:

    def __init__(
        self,
        db_path="data/logs.db"
    ):

        self.conn = sqlite3.connect(
            db_path
        )

        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS footfall_logs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                person_id INTEGER,

                category TEXT,

                gender TEXT,

                age_group TEXT,

                timestamp TEXT
            )
            """
        )

        self.conn.commit()

    def log_person(
        self,
        person_id,
        category,
        gender,
        age_group
    ):

        # Prevent duplicate entries
        self.cursor.execute(
            """
            SELECT person_id
            FROM footfall_logs
            WHERE person_id = ?
            """,
            (person_id,)
        )

        existing = self.cursor.fetchone()

        if existing:
            return

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.cursor.execute(
            """
            INSERT INTO footfall_logs
            (
                person_id,
                category,
                gender,
                age_group,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                person_id,
                category,
                gender,
                age_group,
                timestamp
            )
        )

        self.conn.commit()

    def get_summary(self):

        self.cursor.execute(
            """
            SELECT category,
                   COUNT(*)
            FROM footfall_logs
            GROUP BY category
            """
        )

        return self.cursor.fetchall()

    def close(self):

        self.conn.close()
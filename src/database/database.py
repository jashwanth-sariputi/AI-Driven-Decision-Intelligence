import sqlite3
from datetime import datetime


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            "business_ai.db",
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.create_tables()
        self.ensure_user_columns()

    # ==================================================
    # CREATE TABLES
    # ==================================================

    def create_tables(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS uploads(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                filename TEXT,

                rows INTEGER,

                columns INTEGER,

                dataset_type TEXT,

                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_history(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                dataset_name TEXT,

                model_name TEXT,

                score REAL,

                problem_type TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS prediction_history(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                model_name TEXT,

                filename TEXT,

                rows INTEGER,

                prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE,

                password BLOB,

                email TEXT,

                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                last_login TIMESTAMP

            )
        """)

        self.connection.commit()

    # ==================================================
    # ENSURE OLD DATABASES HAVE NEW USER COLUMNS
    # ==================================================

    def ensure_user_columns(self):

        columns = self.cursor.execute(
            "PRAGMA table_info(users)"
        ).fetchall()

        existing_columns = [
            column[1]
            for column in columns
        ]

        if "email" not in existing_columns:

            self.cursor.execute("""
                ALTER TABLE users
                ADD COLUMN email TEXT
            """)

        if "registered_at" not in existing_columns:

            self.cursor.execute("""
                ALTER TABLE users
                ADD COLUMN registered_at TIMESTAMP
            """)

        if "last_login" not in existing_columns:

            self.cursor.execute("""
                ALTER TABLE users
                ADD COLUMN last_login TIMESTAMP
            """)

        self.connection.commit()

    # ==================================================
    # UPLOAD HISTORY
    # ==================================================

    def save_upload(
        self,
        filename,
        rows,
        columns,
        dataset_type
    ):

        self.cursor.execute("""
            INSERT INTO uploads(
                filename,
                rows,
                columns,
                dataset_type
            )
            VALUES (?, ?, ?, ?)
        """, (
            filename,
            rows,
            columns,
            dataset_type
        ))

        self.connection.commit()

    def get_uploads(self):

        self.cursor.execute("""
            SELECT *
            FROM uploads
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # ==================================================
    # MODEL HISTORY
    # ==================================================

    def save_model(
        self,
        dataset_name,
        model_name,
        score,
        problem_type
    ):

        self.cursor.execute("""
            INSERT INTO model_history(
                dataset_name,
                model_name,
                score,
                problem_type
            )
            VALUES (?, ?, ?, ?)
        """, (
            dataset_name,
            model_name,
            score,
            problem_type
        ))

        self.connection.commit()

    def get_models(self):

        self.cursor.execute("""
            SELECT *
            FROM model_history
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # ==================================================
    # PREDICTION HISTORY
    # ==================================================

    def save_prediction(
        self,
        model_name,
        filename,
        rows
    ):

        self.cursor.execute("""
            INSERT INTO prediction_history(
                model_name,
                filename,
                rows
            )
            VALUES (?, ?, ?)
        """, (
            model_name,
            filename,
            rows
        ))

        self.connection.commit()

    def get_predictions(self):

        self.cursor.execute("""
            SELECT *
            FROM prediction_history
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # ==================================================
    # USER AUTHENTICATION
    # ==================================================

    def create_user(
        self,
        username,
        password,
        email
    ):

        self.cursor.execute("""
            INSERT INTO users(
                username,
                password,
                email,
                registered_at
            )
            VALUES (?, ?, ?, ?)
        """, (
            username,
            password,
            email,
            datetime.now()
        ))

        self.connection.commit()

    # ==================================================
    # GET USER BY USERNAME
    # ==================================================

    def get_user(
        self,
        username
    ):

        self.cursor.execute("""
            SELECT *
            FROM users
            WHERE username = ?
        """, (
            username,
        ))

        return self.cursor.fetchone()

    # ==================================================
    # GET USER BY EMAIL
    # ==================================================

    def get_user_by_email(
        self,
        email
    ):

        self.cursor.execute("""
            SELECT *
            FROM users
            WHERE email = ?
        """, (
            email,
        ))

        return self.cursor.fetchone()

    # ==================================================
    # GET USER PROFILE
    # ==================================================

    def get_user_profile(
        self,
        username
    ):

        self.cursor.execute("""
            SELECT
                id,
                username,
                email,
                registered_at,
                last_login
            FROM users
            WHERE username = ?
        """, (
            username,
        ))

        return self.cursor.fetchone()

    # ==================================================
    # UPDATE LAST LOGIN
    # ==================================================

    def update_last_login(
        self,
        username
    ):

        self.cursor.execute("""
            UPDATE users
            SET last_login = ?
            WHERE username = ?
        """, (
            datetime.now(),
            username
        ))

        self.connection.commit()

    # ==================================================
    # CLOSE DATABASE
    # ==================================================

    def close(self):

        self.connection.close()
import sqlite3


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            "business_ai.db",
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.create_tables()

    # ==================================================
    # Create Tables
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

            password BLOB

        )

        """)

        self.connection.commit()

    # ==================================================
    # Upload History
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

        VALUES(?,?,?,?)

        """, (

            filename,
            rows,
            columns,
            dataset_type

        ))

        self.connection.commit()

    def get_uploads(self):

        self.cursor.execute(

            "SELECT * FROM uploads ORDER BY id DESC"

        )

        return self.cursor.fetchall()

    # ==================================================
    # Model History
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

        VALUES(?,?,?,?)

        """, (

            dataset_name,
            model_name,
            score,
            problem_type

        ))

        self.connection.commit()

    def get_models(self):

        self.cursor.execute(

            "SELECT * FROM model_history ORDER BY id DESC"

        )

        return self.cursor.fetchall()

    # ==================================================
    # Prediction History
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

        VALUES(?,?,?)

        """, (

            model_name,
            filename,
            rows

        ))

        self.connection.commit()

    def get_predictions(self):

        self.cursor.execute(

            "SELECT * FROM prediction_history ORDER BY id DESC"

        )

        return self.cursor.fetchall()

    # ==================================================
    # User Authentication
    # ==================================================

    def create_user(
        self,
        username,
        password
    ):

        self.cursor.execute(

            "INSERT INTO users(username,password) VALUES(?,?)",

            (username, password)

        )

        self.connection.commit()

    def get_user(
        self,
        username
    ):

        self.cursor.execute(

            "SELECT * FROM users WHERE username=?",

            (username,)

        )

        return self.cursor.fetchone()
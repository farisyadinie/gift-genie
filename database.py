import sqlite3


DATABASE = "gift_genie.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    # Enable foreign key relationships
    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_db():

    connection = get_db()


    # ========================================================
    # USERS TABLE
    # ========================================================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT NOT NULL UNIQUE,

            email TEXT NOT NULL UNIQUE,

            password_hash TEXT NOT NULL,

            default_budget
                REAL NOT NULL DEFAULT 100,

            notifications_enabled
                INTEGER NOT NULL DEFAULT 1,

            created_at
                TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # ========================================================
    # CHECK EXISTING USERS TABLE COLUMNS
    # ========================================================

    columns = connection.execute("""
        PRAGMA table_info(users)
    """).fetchall()


    column_names = [
        column["name"]
        for column in columns
    ]


    # ========================================================
    # ADD DEFAULT BUDGET TO OLD USERS TABLE
    # ========================================================

    if "default_budget" not in column_names:

        connection.execute("""
            ALTER TABLE users

            ADD COLUMN
                default_budget
                REAL NOT NULL DEFAULT 100
        """)


    # ========================================================
    # ADD NOTIFICATION SETTING TO OLD USERS TABLE
    # ========================================================

    if "notifications_enabled" not in column_names:

        connection.execute("""
            ALTER TABLE users

            ADD COLUMN
                notifications_enabled
                INTEGER NOT NULL DEFAULT 1
        """)


    # ========================================================
    # RECIPIENTS TABLE
    # ========================================================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS recipients (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            name TEXT NOT NULL,

            relationship TEXT NOT NULL,

            age INTEGER NOT NULL,

            interest TEXT NOT NULL,

            budget REAL NOT NULL,

            created_at
                TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)


    # ========================================================
    # OCCASIONS TABLE
    # ========================================================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS occasions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            recipient_id INTEGER NOT NULL,

            occasion TEXT NOT NULL,

            date TEXT NOT NULL,

            created_at
                TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY (recipient_id)
                REFERENCES recipients(id)
                ON DELETE CASCADE
        )
    """)


    # ========================================================
    # GIFT IDEAS TABLE
    # ========================================================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS gift_ideas (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            recipient_id INTEGER NOT NULL,

            name TEXT NOT NULL,

            description TEXT NOT NULL,

            min_price REAL NOT NULL,

            max_price REAL NOT NULL,

            created_at
                TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY (recipient_id)
                REFERENCES recipients(id)
                ON DELETE CASCADE
        )
    """)


    # ========================================================
    # SAVED GIFTS TABLE
    # ========================================================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS saved_gifts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            gift_idea_id INTEGER NOT NULL,

            recipient_id INTEGER NOT NULL,

            created_at
                TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY (gift_idea_id)
                REFERENCES gift_ideas(id)
                ON DELETE CASCADE,

            FOREIGN KEY (recipient_id)
                REFERENCES recipients(id)
                ON DELETE CASCADE
        )
    """)


    # ========================================================
    # SAVE CHANGES
    # ========================================================

    connection.commit()

    connection.close()
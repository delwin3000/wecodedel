import sqlite3

def migrate_remove_unique_constraint(db_path='instance/site.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Start a transaction
    cursor.execute("BEGIN TRANSACTION;")

    try:
        # Create a new temporary user table without unique constraint on username
        cursor.execute("""
        CREATE TABLE user_temp (
            id INTEGER PRIMARY KEY,
            username VARCHAR(150) NOT NULL,
            password VARCHAR(200) NOT NULL
        );
        """)

        # Copy data from old user table to new user_temp table
        cursor.execute("""
        INSERT INTO user_temp (id, username, password)
        SELECT id, username, password FROM user;
        """)

        # Drop the old user table
        cursor.execute("DROP TABLE user;")

        # Rename user_temp to user
        cursor.execute("ALTER TABLE user_temp RENAME TO user;")

        # Commit the transaction
        conn.commit()
        print("Migration completed successfully: unique constraint on username removed.")
    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_remove_unique_constraint()

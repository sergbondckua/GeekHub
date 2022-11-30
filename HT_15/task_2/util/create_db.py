"""Create DB"""
import sqlite3


def create_db():
    """Create DB for ATM"""

    connect_sql = sqlite3.connect("rozetka.db")
    try:
        with connect_sql:
            cursor = connect_sql.cursor()

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS products(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INT,
                    title TEXT,
                    old_price INT,
                    price INT,
                    href TEXT,
                    brand TEXT,
                    category TEXT)"""
            )

            connect_sql.commit()
            print("[INFO] Table created successfully")
    except sqlite3.Error as ex:
        print("[INFO] Error while working with SQLite3", ex)
    finally:
        if connect_sql:
            connect_sql.close()
            print("[INFO] SQLite3 connection closed")


if __name__ == '__main__':
    create_db()

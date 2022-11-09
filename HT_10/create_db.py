import sqlite3


def create_db():
    """Create DB for ATM"""

    connect_sql = sqlite3.connect("atm.db")
    try:
        with connect_sql:
            cursor = connect_sql.cursor()

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT,
                    balance INT,
                    staff TEXT)"""
            )
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS statement(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    orders TEXT)"""
            )
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS money_bills(
                    bill INT PRIMARY KEY,
                    count INT)"""
            )

            users = [
                ('1', 'user1', 'user1', '0', 'client'),
                ('2', 'user2', 'user2', '0', 'client'),
                ('3', 'admin', 'admin', '0', 'collector')
            ]

            bills = [(10, 100),
                     (20, 50),
                     (50, 50),
                     (100, 50),
                     (200, 50),
                     (500, 100),
                     (1000, 100)
                     ]
            cursor.executemany("INSERT INTO users VALUES (?,?,?,?,?)", users)
            cursor.executemany("INSERT INTO money_bills VALUES (?,?)", bills)

            connect_sql.commit()
            print("[INFO] Table created successfully")
    except Exception as ex:
        print("[INFO] Error while working with SQLite3", ex)
    finally:
        if connect_sql:
            connect_sql.close()
            print("[INFO] SQLite3 connection closed")


if __name__ == '__main__':
    create_db()

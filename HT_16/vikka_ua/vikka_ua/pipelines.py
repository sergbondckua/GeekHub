"""Define your item pipelines here

Don't forget to add your pipeline to the ITEM_PIPELINES setting
See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html"""

# useful for handling different item types with a single interface
import sqlite3


class VikkaUaPipeline:
    """Create and / or save a new scrape"""

    def __init__(self):
        self.create_conn()
        self.create_table()

    def create_conn(self):
        """Create connection to database"""
        self.conn = sqlite3.connect("out_files/vikka_news.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        """Create table method"""
        self.curr.execute("""DROP TABLE IF EXISTS news_item""")
        self.curr.execute(
            """CREATE TABLE
                news_item(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time_pub TEXT,
                    title TEXT,
                    full_text TEXT,
                    tags TEXT,
                    url TEXT)
            """)

    def process_item(self, item, spider):
        """Store items to databases."""
        self.curr.execute(
            """
            INSERT INTO news_item (time_pub, title, full_text, tags, url)
            VALUES (?,?,?,?,?)""",
            (
                item['time_pub'],
                item['title'],
                item['text'],
                item['tags'],
                item['url'],
            )
        )
        self.conn.commit()
        return item

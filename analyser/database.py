import sqlite3
import os
import sys

def create_db():
    HERE = os.path.dirname(sys.argv[0])

    conn = sqlite3.connect(os.path.join(HERE, '..', 'files', 'detected_text.db'))
    c = conn.cursor()

    c.execute(
    """
    CREATE TABLE IF NOT EXISTS texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        img_id TEXT,
        extension TEXT,
        text TEXT
    );
    """
    )

    conn.commit()

def insert_text(conn, cursor, img_id, extension, text):
    sql = "INSERT INTO texts (img_id, extension, text) VALUES (?,?,?);"
    vals = (img_id, extension, text)
    cursor.execute(sql, vals)
    conn.commit()

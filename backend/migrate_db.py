import os
import sqlite3
import pymysql
from dotenv import load_dotenv

load_dotenv()

# 接続情報の確認（デバッグ用）
print("HOST:", os.getenv("DB_HOST"))
print("USER:", os.getenv("DB_USER"))
print("DB:  ", os.getenv("DB_NAME"))

sqlite_conn = sqlite3.connect("tech0_search.db")
sqlite_conn.row_factory = sqlite3.Row
rows = sqlite_conn.execute("select title, url, body from pages").fetchall()

mysql_conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    charset="utf8mb4",
    connect_timeout=10,
    ssl={"verify_cert": False},  # 証明書検証なしでSSL接続
)

cursor = mysql_conn.cursor()
for row in rows:
    cursor.execute(
        "INSERT IGNORE INTO pages (title, url, body) VALUES (%s, %s, %s)",
        (row["title"], row["url"], row["body"]),
    )
mysql_conn.commit()
print(f"移行完了: {len(rows)} 件のデータを移行しました。")
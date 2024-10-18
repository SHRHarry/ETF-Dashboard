import sqlite3

# 資料庫連接函數
def get_db_connection():
    conn = sqlite3.connect('etf_holdings.db')
    conn.row_factory = sqlite3.Row  # 以行為基礎返回字典
    return conn

# 建立資料庫表格
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS holdings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        purchase_date TEXT NOT NULL,
        symbol TEXT NOT NULL,
        shares INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
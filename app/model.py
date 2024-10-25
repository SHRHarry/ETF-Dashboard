import sqlite3
from fastapi import HTTPException

class SqlHandler:
    def __init__(self):
        self._create_tables()
    
    def select_all_data(self):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM holdings')
        holdings = cursor.fetchall()
        conn.close()
        return holdings
    
    def select_by_symbol(self, symbol):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM holdings WHERE symbol = ?', (symbol,))
        holdings = cursor.fetchall()
        conn.close()
        return holdings
    
    def insert_data(self, stock):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO holdings (purchase_date, symbol, shares) 
        VALUES (?, ?, ?)
        ''', (stock.purchase_date.isoformat(), stock.symbol, stock.shares))
        conn.commit()
        conn.close()
    
    def edit_data(self, stock_id, stock):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE holdings
            SET shares = ?, purchase_date = ?
            WHERE id = ?
        ''', (stock.shares, stock.purchase_date, stock_id))
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Stock not found")
        
        conn.commit()
        conn.close()
    
    def delete_all_data(self):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM holdings')
        conn.commit()
        conn.close()
    
    def delete_by_symbol(self, symbol):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM holdings WHERE symbol = ?', (symbol,))
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Stock not found")
        conn.commit()
        conn.close()
    
    def _create_tables(self):
        conn = self._get_db_connection()
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
    
    def _get_db_connection(self):
        conn = sqlite3.connect('etf_holdings.db')
        conn.row_factory = sqlite3.Row  # 以行為基礎返回字典
        return conn
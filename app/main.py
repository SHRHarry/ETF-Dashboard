from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

from app.model import get_db_connection, create_tables
from app.dividends_calculator import calc_total_dividends

app = FastAPI()
create_tables()

# Pydantic 模型，用於增加股數時的請求數據
class StockUpdate(BaseModel):
    symbol: str
    shares: int
    purchase_date: datetime

# 1. 取得總股利
@app.get("/total_dividends")
def get_total_dividends():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM holdings')
    holdings = cursor.fetchall()
    conn.close()
    total_dividends = calc_total_dividends(holdings)
    
    return {"total_dividends": total_dividends or 0}

# 2. 取得個別股票的股利
@app.get("/individual_stock_dividends")
def get_individual_stock_dividends(symbol: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT shares, dividend FROM holdings WHERE symbol = ?', (symbol,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Stock not found")
    total_dividend = sum(row["shares"] * row["dividend"] for row in rows)
    return {"symbol": symbol, "total_dividend": total_dividend}

# 3. 增加個別股票的股數
@app.post("/individual_stock_dividends")
def add_stock(stock: StockUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO holdings (purchase_date, symbol, shares) 
    VALUES (?, ?, ?)
    ''', (stock.purchase_date.isoformat(), stock.symbol, stock.shares))
    conn.commit()
    conn.close()
    return {"message": "Stock added successfully"}
    
    # if stock_update.symbol not in holdings:
    #     raise HTTPException(status_code=404, detail="Stock not found")
    # holdings[stock_update.symbol]["shares"] += stock_update.shares
    # return {"symbol": stock_update.symbol, "new_shares": holdings[stock_update.symbol]["shares"]}

# 4. 刪除個別股票的股數
@app.delete("/individual_stock_dividends")
def delete_individual_stock(symbol: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM holdings WHERE symbol = ?', (symbol,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Stock not found")
    conn.commit()
    conn.close()
    return {"message": f"Stock with symbol {symbol} deleted successfully"}

# 5. 刪除全部股數
@app.delete("/total_dividends")
def delete_all_stocks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM holdings')
    conn.commit()
    conn.close()
    return {"message": "All stocks deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    # uvicorn.run("your_filename:app", host="0.0.0.0", port=8000, reload=True)
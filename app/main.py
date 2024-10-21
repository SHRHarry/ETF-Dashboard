from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from app.model import get_db_connection, create_tables
from app.dividends_calculator import calc_total_dividends, calc_individual_stock_dividends

app = FastAPI()
create_tables()

# 配置 CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 你可以具體設置前端應用的URL，例如 'http://localhost:3000'
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有 HTTP 標頭
)

# Pydantic 模型，用於增加股數時的請求數據
class StockUpdate(BaseModel):
    symbol: str
    shares: int
    purchase_date: datetime

# 1. 取得總股利
@app.get("/total_dividends")
async def get_total_dividends():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM holdings')
    holdings = cursor.fetchall()
    conn.close()
    total_dividends = calc_total_dividends(holdings)
    
    return {"total_dividends": total_dividends or 0}

# 2. 取得個別股票的股利
@app.get("/individual_stock_dividends")
async def get_individual_stock_dividends(symbol: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM holdings WHERE symbol = ?', (symbol,))
    holdings = cursor.fetchall()
    conn.close()
    if not holdings:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    receive_dividends, receive_shares = calc_individual_stock_dividends(holdings)
    
    return {"symbol": symbol, "receive_dividends": receive_dividends, "receive_shares": receive_shares}

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
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from app.model import SqlHandler
from app.dividends_calculator import calc_total_dividends, calc_individual_stock_dividends

app = FastAPI()
sql_handler = SqlHandler()

# CORS Configs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 你可以具體設置前端應用的URL，例如 'http://localhost:3000'
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有 HTTP 標頭
)

# Pydantic Model for Data Validation
class StockUpdate(BaseModel):
    symbol: str
    shares: int
    purchase_date: datetime

@app.get("/total_dividends")
async def get_total_dividends():
    holdings = sql_handler.select_all_data()
    total_dividends = calc_total_dividends(holdings)
    
    return {"total_dividends": total_dividends or 0}

@app.get("/individual_stock_dividends")
async def get_individual_stock_dividends(symbol: str):
    holdings = sql_handler.select_by_symbol(symbol)
    if not holdings:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    for h in holdings:
        print(h["id"])
    receive_dividends, receive_shares = calc_individual_stock_dividends(holdings)
    
    return {"symbol": symbol, "receive_dividends": receive_dividends, "receive_shares": receive_shares}

@app.get("/all_stocks")
async def get_all_stocks():
    holdings = sql_handler.select_all_data()
    
    if not holdings:
        return []

    return [{"id": holding["id"], "symbol": holding["symbol"], "shares": holding["shares"], "purchase_date": holding["purchase_date"]}
            for holding in holdings]

@app.post("/individual_stock_dividends")
def add_stock(stock: StockUpdate):
    sql_handler.insert_data(stock)
    return {"message": "Stock added successfully"}

@app.put("/individual_stock_dividends/{stock_id}")
async def update_individual_stock(stock_id: int, stock: StockUpdate):
    sql_handler.edit_data(stock_id, stock)
    return {"message": f"Stock with id {stock_id} updated successfully"}

@app.delete("/individual_stock_dividends")
def delete_individual_stock(symbol: str):
    sql_handler.delete_by_symbol(symbol)
    return {"message": f"Stock with symbol {symbol} deleted successfully"}

@app.delete("/total_dividends")
def delete_all_stocks():
    sql_handler.delete_all_data()
    return {"message": "All stocks deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    # uvicorn.run("your_filename:app", host="0.0.0.0", port=8000, reload=True)
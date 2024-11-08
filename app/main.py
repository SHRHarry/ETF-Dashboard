from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from app.model import SqlHandler
from app.dividends_calculator import calc_total_dividends, calc_individual_stock_dividends, calc_dividends_curr_month

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
def get_total_dividends():
    holdings = sql_handler.select_all_data()
    if not holdings:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    total_dividends = calc_total_dividends(holdings)
    
    return {"total_dividends": total_dividends or 0}

@app.get("/individual_stock_dividends")
def get_individual_stock_dividends(symbol: str):
    holdings = sql_handler.select_by_symbol(symbol)
    if not holdings:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    receive_dividends, receive_shares = calc_individual_stock_dividends(holdings)
    
    return {"symbol": symbol, "receive_dividends": receive_dividends, "receive_shares": receive_shares}

@app.get("/individual_stock_dividends/{stock_id}")
def get_individual_stock(stock_id: int):
    holding = sql_handler.select_by_id(stock_id)
    if not holding:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    return {"id": holding[0]["id"], "symbol": holding[0]["symbol"], "shares": holding[0]["shares"], "purchase_date": holding[0]["purchase_date"]}

@app.get("/all_stocks")
def get_all_stocks():
    holdings = sql_handler.select_all_data()
    
    if not holdings:
        return []

    return [{"id": holding["id"], "symbol": holding["symbol"], "shares": holding["shares"], "purchase_date": holding["purchase_date"]}
            for holding in holdings]

@app.get("/curr_month_dividends")
def get_curr_month_dividends():
    holdings = sql_handler.select_all_data()
    if not holdings:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    curr_month_dividends = calc_dividends_curr_month(holdings)
    return curr_month_dividends

@app.post("/individual_stock_dividends")
def add_stock(stock: StockUpdate):
    sql_handler.insert_data(stock)
    return {"message": "Stock added successfully"}

@app.put("/individual_stock_dividends/{stock_id}")
def update_individual_stock(stock_id: int, stock: StockUpdate):
    sql_handler.edit_data(stock_id, stock)
    return {"message": f"Stock with id {stock_id} updated successfully"}

@app.delete("/individual_stock_dividends/{stock_id}")
def delete_individual_stock(stock_id: int):
    sql_handler.delete_by_id(stock_id)
    return {"message": f"Stock with stock_id {stock_id} deleted successfully"}

@app.delete("/total_dividends")
def delete_all_stocks():
    sql_handler.delete_all_data()
    return {"message": "All stocks deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    # uvicorn.run("your_filename:app", host="0.0.0.0", port=8000, reload=True)
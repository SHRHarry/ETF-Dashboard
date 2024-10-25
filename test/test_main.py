import sys
sys.path.insert(0, './')
from fastapi.testclient import TestClient

from app.main import app, StockUpdate
from app.model import SqlHandler

client = TestClient(app)

def test_get_total_dividends():
    # 假設初始資料庫已經有相關的數據
    response = client.get("/total_dividends")
    assert response.status_code == 200
    data = response.json()
    assert "total_dividends" in data
    assert data["total_dividends"] >= 0  # 確保總股利為正值

def test_add_stock_shares():
    stock_data = {"symbol": "00919", "shares": 500, "purchase_date": "2024-03-14"}
    response = client.post("/individual_stock_dividends", json=stock_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Stock added successfully"
    
def test_get_individual_stock_dividends():
    sql_handler = SqlHandler()
    sql_handler.insert_data(StockUpdate(symbol="0056", shares=1000, purchase_date="2024-03-14"))
    
    stock_data = {"symbol": "0056"}
    response = client.get("/individual_stock_dividends", params=stock_data)
    assert response.status_code == 200
    data = response.json()
    assert "receive_dividends" in data
    assert data["receive_dividends"] >= 0  # 確保個別股票的股利為正值
    assert "receive_shares" in data
    assert data["receive_shares"] >= 0  # 確保個別股票的股利為正值

def test_delete_stock_shares():
    stock_data = {"symbol": "00919"}
    response = client.delete("/individual_stock_dividends", params=stock_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Stock with symbol {stock_data['symbol']} deleted successfully"

def test_delete_all_stocks():
    response = client.delete("/total_dividends")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "All stocks deleted successfully"
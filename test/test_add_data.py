import requests
import json

def test_add_fake_data():
    holdings = [
        {'purchase_date': '2024-03-14', 'symbol': '00878', 'shares': 1000},
        {'purchase_date': '2024-03-14', 'symbol': '0056', 'shares': 1000},
        {'purchase_date': '2024-03-14', 'symbol': '00919', 'shares': 1000},
        {'purchase_date': '2024-04-17', 'symbol': '0056', 'shares': 1000},
        {'purchase_date': '2024-05-15', 'symbol': '00878', 'shares': 1000},
        {'purchase_date': '2024-05-22', 'symbol': '00919', 'shares': 1000},
        {'purchase_date': '2024-06-06', 'symbol': '00919', 'shares': 1000}
    ]
    api_url = "http://127.0.0.1:8000/individual_stock_dividends"
    for h in holdings:
        response = requests.post(api_url, data=json.dumps(h))
    
        res_json = response.json()
        print(f"test_add_fake_data | {res_json}")

if __name__ == '__main__':
    test_add_fake_data()
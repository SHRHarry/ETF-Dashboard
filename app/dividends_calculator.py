import time
import requests
import datetime
import numpy as np 
import pandas as pd
from bs4 import BeautifulSoup
from fastapi import HTTPException

def process_data_by_symbol(holdings):
    processed_holdings = {}
    for h in holdings:
        h = dict(h)
        if h["symbol"] not in processed_holdings:
            processed_holdings[h["symbol"]] = [h]
        else:
            processed_holdings[h["symbol"]].append(h)
        
    return processed_holdings

def get_dividend_list(symbol, retries=3, delay=1):
    div_url = f'https://www.moneydj.com/ETF/X/Basic/Basic0005.xdjhtm?etfid={symbol}.TW'
    for attempt in range(retries):
        try:
            r = requests.get(div_url)
            r.raise_for_status()  # 若狀態碼非200，將拋出HTTPError
            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.findAll("table", class_="datalist")[0]
            
            list_rows = []
            rows = table.find_all('tr')
            
            for row in rows:
                row_td = [i.text for i in row.find_all('td')]
                if len(row_td)>1:
                    list_rows.append(np.array(row_td)[[0,1,7]])
                    
            df = pd.DataFrame(list_rows, columns = ['ex_div_date','pay_date','div_amount'])
            df['symbol_id'] = [symbol] * len(df)
            
            return df
        except (requests.exceptions.HTTPError, IndexError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)  # 重試前的延遲
    # 如果多次嘗試後仍失敗
    raise HTTPException(status_code=404, detail="Unable to retrieve data after multiple attempts.")

def calc_dividends_curr_month(holdings):
    dividends_curr_month = {}
    holdings = process_data_by_symbol(holdings)
    
    today = datetime.datetime.today()
    # today = datetime.datetime.strptime("202407", "%Y%m")

    for key, lst in holdings.items():
        symbol = key
        df = get_dividend_list(symbol)
        df['ex_div_date'] = pd.to_datetime(df['ex_div_date'])
        eligible_dividends = df[(df['ex_div_date'].dt.month == today.month) & (df['ex_div_date'].dt.year == today.year)]
        curr_shares = 0
        curr_dividends = 0
        for dic in lst:
            curr_shares += dic['shares']
        
        for _, row in eligible_dividends.iterrows():
            curr_dividends = float(row['div_amount'])*curr_shares
        
        if curr_dividends > 0:
            dividends_curr_month[key] = curr_dividends
    
    return dividends_curr_month

def calc_total_dividends(holdings):
    total_dividends = 0
    holdings = process_data_by_symbol(holdings)
    
    for key, lst in holdings.items():
        symbol = key
        df = get_dividend_list(symbol)
        df['ex_div_date'] = pd.to_datetime(df['ex_div_date'])
        
        # dividend_symbol = 0
        for dic in lst:
            purchase_date = pd.to_datetime(dic['purchase_date'])
            shares = dic['shares']
        
            # 篩選除息日 >= 購買日
            eligible_dividends = df[df['ex_div_date'] >= purchase_date]
            # print(f"eligible_dividends = {eligible_dividends}")
        
            # 計算股利
            for _, row in eligible_dividends.iterrows():
                dividend = float(row['div_amount']) * shares
                total_dividends += dividend
                # dividend_symbol += dividend
            
        # print(f"股票代號: {symbol}, 獲得股利: {dividend_symbol}")
    
    # print(f"總股利: {total_dividends}")
    return total_dividends

def calc_individual_stock_dividends(holdings):
    individual_dividends = 0
    individual_shares = 0
    
    holdings = process_data_by_symbol(holdings)
    symbol = next(iter(holdings.keys()))
    df = get_dividend_list(symbol)
    df['ex_div_date'] = pd.to_datetime(df['ex_div_date'])
    
    for dic in next(iter(holdings.values())):
        purchase_date = pd.to_datetime(dic['purchase_date'])
        shares = dic['shares']
        individual_shares += shares
    
        # 篩選除息日 >= 購買日
        eligible_dividends = df[df['ex_div_date'] >= purchase_date]
    
        # 計算股利
        for _, row in eligible_dividends.iterrows():
            dividend = float(row['div_amount']) * shares
            individual_dividends += dividend
    
    return individual_dividends, individual_shares

if __name__ == "__main__":
    holdings = [
        {'purchase_date': '2024-03-14', 'symbol': '00878', 'shares': 1000},
        {'purchase_date': '2024-03-14', 'symbol': '0056', 'shares': 1000},
        {'purchase_date': '2024-03-14', 'symbol': '00919', 'shares': 1000},
        {'purchase_date': '2024-04-17', 'symbol': '0056', 'shares': 1000},
        {'purchase_date': '2024-05-15', 'symbol': '00878', 'shares': 1000},
        {'purchase_date': '2024-05-22', 'symbol': '00919', 'shares': 1000},
        {'purchase_date': '2024-06-06', 'symbol': '00919', 'shares': 1000}
    ]
    # holdings = [
    #     {'purchase_date': '2021/9/10', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2021/10/10', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2021/11/10', 'symbol': '00878', 'shares': 1000},
    #     {'purchase_date': '2021/12/10', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2022/1/10', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2022/2/10', 'symbol': '00878', 'shares': 1000},
    #     {'purchase_date': '2022/3/14', 'symbol': '00878', 'shares': 1000},
    #     {'purchase_date': '2022/3/14', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2022/3/14', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2022/4/17', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2022/5/15', 'symbol': '00878', 'shares': 1000},
    #     {'purchase_date': '2022/5/22', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2022/6/6', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2022/7/6', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2022/8/6', 'symbol': '00878', 'shares': 1000},
        
    #     {'purchase_date': '2022/9/10', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2022/10/10', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2022/11/10', 'symbol': '00878', 'shares': 1000},
    #     {'purchase_date': '2022/12/10', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2023/1/10', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2023/2/10', 'symbol': '00878', 'shares': 1000},
    #     {'purchase_date': '2023/3/14', 'symbol': '00878', 'shares': 1000},
    #     {'purchase_date': '2023/3/14', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2023/3/14', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2023/4/17', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2023/5/15', 'symbol': '00878', 'shares': 1000},
    #     {'purchase_date': '2023/5/22', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2023/6/6', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2023/7/6', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2023/8/6', 'symbol': '00878', 'shares': 1000},
        
    #     {'purchase_date': '2023/9/10', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2023/10/10', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2023/11/10', 'symbol': '00878', 'shares': 1000},
    #     {'purchase_date': '2023/12/10', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2024/1/10', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2024/2/10', 'symbol': '00878', 'shares': 1000},
    #     {'purchase_date': '2024/3/14', 'symbol': '00878', 'shares': 1000},
    #     {'purchase_date': '2024/3/14', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2024/3/14', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2024/4/17', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2024/5/15', 'symbol': '00878', 'shares': 1000},
    #     {'purchase_date': '2024/5/22', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2024/6/6', 'symbol': '00919', 'shares': 1000},
    #     {'purchase_date': '2024/7/6', 'symbol': '0056', 'shares': 1000},
    #     {'purchase_date': '2024/8/6', 'symbol': '00878', 'shares': 1000},
    #     {'purchase_date': '2024/9/6', 'symbol': '00919', 'shares': 1000}
    # ]
    calc_total_dividends(holdings)
    calc_dividends_curr_month(holdings)
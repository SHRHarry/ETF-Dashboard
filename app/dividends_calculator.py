import requests 
import numpy as np 
import pandas as pd
from bs4 import BeautifulSoup

def process_data_by_symbol(holdings):
    processed_holdings = {}
    for h in holdings:
        h = dict(h)
        if h["symbol"] not in processed_holdings:
            processed_holdings[h["symbol"]] = [h]
        else:
            processed_holdings[h["symbol"]].append(h)
        
    return processed_holdings

def get_dividend_list(symbol):     
    div_url = f'https://www.moneydj.com/ETF/X/Basic/Basic0005.xdjhtm?etfid={symbol}.TW'
    r = requests.get(div_url)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.findAll("table", class_ = "datalist")[0]

    list_rows = []
    rows = table.find_all('tr')
    
    for row in rows:
        row_td = [i.text for i in row.find_all('td')]
        if len(row_td)>1:
            list_rows.append(np.array(row_td)[[0,1,7]])
            
    df = pd.DataFrame(list_rows, columns = ['ex_div_date','pay_date','div_amount'])
    df['symbol_id'] = [symbol] * len(df)
    
    return df

def calc_total_dividends(holdings):
    total_dividends = 0
    holdings = process_data_by_symbol(holdings)
    
    for key, lst in holdings.items():
        # 查詢股利資料
        symbol = key
        df = get_dividend_list(symbol)
        df['ex_div_date'] = pd.to_datetime(df['ex_div_date'])
        
        dividend_symbol = 0
        for dic in lst:
            purchase_date = pd.to_datetime(dic['purchase_date'])
            shares = dic['shares']
        
            # 篩選除息日 >= 購買日
            eligible_dividends = df[df['ex_div_date'] >= purchase_date]
        
            # 計算股利
            for _, row in eligible_dividends.iterrows():
                dividend = float(row['div_amount']) * shares
                total_dividends += dividend
                dividend_symbol += dividend
            
        print(f"股票代號: {symbol}, 獲得股利: {dividend_symbol}")
    
    print(f"總股利: {total_dividends}")
    return total_dividends

def get_total_shares(holdings):
    # 用字典來儲存每個股票代號的總股數
    share_count = {}

    for holding in holdings:
        symbol = holding['symbol']
        shares = holding['shares']
        
        if symbol in share_count:
            share_count[symbol] += shares
        else:
            share_count[symbol] = shares

    # 打印每個股票的總股數
    for symbol, total_shares in share_count.items():
        print(f"股票代號: {symbol}, 總股數: {total_shares}")
    
    # 或者返回結果
    return share_count

if __name__ == "__main__":
    # 購買資料
    holdings = [
        {'purchase_date': '2024/3/14', 'symbol': '00878', 'shares': 1000},
        {'purchase_date': '2024/3/14', 'symbol': '0056', 'shares': 1000},
        {'purchase_date': '2024/3/14', 'symbol': '00919', 'shares': 1000},
        {'purchase_date': '2024/4/17', 'symbol': '0056', 'shares': 1000},
        {'purchase_date': '2024/5/15', 'symbol': '00878', 'shares': 1000},
        {'purchase_date': '2024/5/22', 'symbol': '00919', 'shares': 1000},
        {'purchase_date': '2024/6/6', 'symbol': '00919', 'shares': 1000}
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
    get_total_shares(holdings)
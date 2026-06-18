# binance_data.py
import requests
import pandas as pd

BASE = "https://fapi.binance.com"

def get_filtered_symbols():
    url = f"{BASE}/fapi/v1/ticker/24hr"
    data = requests.get(url).json()
    symbols = []
    for t in data:
        sym = t['symbol']
        if not sym.endswith('USDT'):
            continue
        try:
            if float(t['quoteVolume']) >= 1_000_000:
                symbols.append(sym)
        except:
            continue
    return symbols

def get_klines(symbol, interval="1d", limit=150):
    url = f"{BASE}/fapi/v1/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    data = requests.get(url, params=params).json()
    df = pd.DataFrame(data, columns=[
        'time','open','high','low','close','volume',
        'close_time','qv','trades','tbbav','tbqav','ignore'
    ])
    for col in ['open','high','low','close','volume']:
        df[col] = df[col].astype(float)
    return df
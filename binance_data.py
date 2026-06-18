# binance_data.py
import requests
import pandas as pd

SPOT_BASE = "https://api.binance.com"
FUTURES_BASE = "https://fapi.binance.com"

def get_filtered_symbols():
    url = f"{FUTURES_BASE}/fapi/v1/ticker/24hr"
    response = requests.get(url, timeout=10)
    data = response.json()
    print(f"API javob turi: {type(data)}, uzunlik: {len(data) if isinstance(data, list) else 'dict'}")
    if isinstance(data, dict):
        print(f"API xatosi: {data}")
        return []
    symbols = []
    for t in data:
        sym = t.get('symbol', '')
        if not sym.endswith('USDT'):
            continue
        try:
            if float(t.get('quoteVolume', 0)) >= 1_000_000:
                symbols.append(sym)
        except:
            continue
    print(f"Topilgan symbollar: {len(symbols)}")
    return symbols

def get_klines(symbol, interval="1d", limit=150):
    url = f"{FUTURES_BASE}/fapi/v1/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    data = requests.get(url, params=params, timeout=10).json()
    df = pd.DataFrame(data, columns=[
        'time','open','high','low','close','volume',
        'close_time','qv','trades','tbbav','tbqav','ignore'
    ])
    for col in ['open','high','low','close','volume']:
        df[col] = df[col].astype(float)
    return df
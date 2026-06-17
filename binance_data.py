# binance_data.py
from binance.client import Client
import pandas as pd

client = Client()  # API key shart emas (public endpoints)

def get_filtered_symbols():
    """Kunlik hajmi $1M dan oshiq USDT spot coinlarini qaytaradi"""
    tickers = client.get_ticker()
    symbols = []
    for t in tickers:
        sym = t['symbol']
        if not sym.endswith('USDT'):
            continue
        try:
            volume_usdt = float(t['quoteVolume'])
            if volume_usdt >= 1_000_000:
                symbols.append(sym)
        except:
            continue
    return symbols

def get_klines(symbol, interval="1d", limit=150):
    """Oxirgi 150 kunlik OHLCV ma'lumotlarini DataFrame sifatida qaytaradi"""
    raw = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(raw, columns=[
        'time','open','high','low','close','volume',
        'close_time','qv','trades','tbbav','tbqav','ignore'
    ])
    for col in ['open','high','low','close','volume']:
        df[col] = df[col].astype(float)
    return df
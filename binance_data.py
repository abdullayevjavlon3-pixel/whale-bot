# binance_data.py
import ccxt
import pandas as pd

exchange = ccxt.binance({
    'options': {'defaultType': 'spot'},
})

def get_filtered_symbols():
    tickers = exchange.fetch_tickers()
    symbols = []
    for sym, t in tickers.items():
        if not sym.endswith('/USDT'):
            continue
        try:
            volume_usdt = float(t['quoteVolume'] or 0)
            if volume_usdt >= 1_000_000:
                symbols.append(sym.replace('/USDT', 'USDT'))
        except:
            continue
    return symbols

def get_klines(symbol, interval="1d", limit=150):
    ccxt_symbol = symbol.replace('USDT', '/USDT')
    ohlcv = exchange.fetch_ohlcv(ccxt_symbol, timeframe=interval, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['time','open','high','low','close','volume'])
    return df
    
# signal.py
import numpy as np
import pandas as pd

def xsa(src: pd.Series, length: int, weight: float) -> pd.Series:
    """Wilder smoothing: SMA dan boshlanib EMA ga o'tadi"""
    result = [np.nan] * len(src)
    sumf = 0.0
    for i in range(len(src)):
        sumf = sumf - (src.iloc[i - length] if i >= length else 0) + src.iloc[i]
        ma = sumf / length if i >= length - 1 else np.nan
        if np.isnan(result[i - 1]) if i > 0 else True:
            result[i] = ma
        else:
            result[i] = (src.iloc[i] * weight + result[i-1] * (length - weight)) / length
    return pd.Series(result, index=src.index)

def calculate_kdj(df: pd.DataFrame, n=18, m1=4, m2=4):
    """KDJ indikatorini hisoblaydi"""
    low_min  = df['low'].rolling(n).min()
    high_max = df['high'].rolling(n).max()
    rsv = (df['close'] - low_min) / (high_max - low_min + 1e-10) * 100
    K = xsa(rsv, m1, 1)
    D = xsa(K, m2, 1)
    J = 3 * K - 2 * D
    return K, D, J

def calculate_whale_pump(df: pd.DataFrame):
    """Whale Pump signalini hisoblaydi — sariq sham paydo bo'lsa > 0"""
    low  = df['low']
    close = df['close']

    # xrf: oldingi barning low qiymati (shift(1))
    var1 = low.shift(1)

    # Nisbiy tebranish (0-100 oralig'ida)
    diff = (low - var1).abs()
    pos  = (low - var1).clip(lower=0)

    s_diff = diff.rolling(3).mean()
    s_pos  = pos.rolling(3).mean()
    var2   = (s_diff / s_pos.replace(0, np.nan) * 100).fillna(0)

    # EMA: close har doim 0 dan katta, shart har doim True → var2 * 10
    var3 = (var2 * 10).ewm(span=3, adjust=False).mean()

    # 38 barlik min/max
    var4 = low.rolling(38).min()
    var5 = var3.rolling(38).max()

    # 90 barlik global minimum trigger
    lowest_90 = low.rolling(90).min()
    var6 = (low <= lowest_90).astype(float)

    # Whale pump qiymati
    condition = (low <= var4).astype(float)
    inner = condition * (var3 + var5 * 2) / 2
    var7 = inner.ewm(span=3, adjust=False).mean() / 618 * var6

    return var7

def get_signal(df: pd.DataFrame):
    """
    Oxirgi barda whale pump > 0 bo'lsa signal qaytaradi.
    Return: dict yoki None
    """
    K, D, J = calculate_kdj(df)
    wp = calculate_whale_pump(df)

    last_wp = wp.iloc[-1]
    if last_wp > 0:
        return {
            'whale_pump': round(last_wp, 4),
            'K': round(K.iloc[-1], 2),
            'D': round(D.iloc[-1], 2),
            'J': round(J.iloc[-1], 2),
            'close': df['close'].iloc[-1],
            'volume': df['volume'].iloc[-1],
        }
    return None
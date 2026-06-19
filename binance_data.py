def get_klines(symbol, interval="1d", limit=150):
    url = f"{SPOT_BASE}/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError(f"Klines bo'sh yoki xato: {data}")
    df = pd.DataFrame(data, columns=[
        'time','open','high','low','close','volume',
        'close_time','qv','trades','tbbav','tbqav','ignore'
    ])
    for col in ['open','high','low','close','volume']:
        df[col] = df[col].astype(float)
    return df
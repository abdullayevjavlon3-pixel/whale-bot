# main.py
import asyncio
import schedule
import time
from binance_data import get_filtered_symbols, get_klines
from whale_signal import get_signal
from bot import send_signal, send_status
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

# Takrorlanishni oldini olish uchun
seen_signals = {"15m": set(), "1h": set(), "4h": set()}

TIMEFRAMES = {
    "15m": 500,   # 15 daqiqa
    "1h":  500,   # 1 soat
    "4h":  500,   # 4 soat
}

async def scan_timeframe(interval: str, limit: int, symbols: list):
    found = 0
    for symbol in symbols:
        try:
            df = get_klines(symbol, interval=interval, limit=limit)
            result = get_signal(df)
            if result:
                key = f"{symbol}_{interval}_{df['time'].iloc[-1]}"
                if key not in seen_signals[interval]:
                    seen_signals[interval].add(key)
                    result['interval'] = interval
                    await send_signal(symbol, result)
                    found += 1
                    await asyncio.sleep(0.5)  # 0.3 dan 0.5 ga
        except Exception as e:
            print(f"{symbol} [{interval}] xatosi: {e}")
    return found

async def scan_all(interval: str):
    print(f"\n[{interval}] Skanerlash boshlandi...")
    symbols = get_filtered_symbols()
    print(f"[{interval}] Coinlar: {len(symbols)}")
    found = await scan_timeframe(interval, TIMEFRAMES[interval], symbols)
    msg = f"[{interval}] {len(symbols)} ta coin, {found} ta signal"
    print(msg)
    if found > 0:
        await send_status(msg)

def run_scan(interval: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(scan_all(interval))
    finally:
        loop.close()

if __name__ == "__main__":
    print("Bot ishga tushdi. 15m / 1h / 4h skanerlaydi.")
    asyncio.run(send_status("Bot ishga tushdi!\n15m / 1h / 4h timeframelarda ishlaydi."))

    # Har 15 daqiqada
    schedule.every(15).minutes.do(run_scan, interval="15m")

    # Har 1 soatda
    schedule.every(1).hours.do(run_scan, interval="1h")

    # Har 4 soatda
    schedule.every(4).hours.do(run_scan, interval="4h")

    # Darhol bir marta ishga tushirish
    run_scan("15m")
    run_scan("1h")
    run_scan("4h")

    while True:
        schedule.run_pending()
        time.sleep(30)
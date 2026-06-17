# bot.py
import asyncio
from telegram import Bot
from datetime import datetime
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(token=TELEGRAM_TOKEN)

async def send_signal(symbol: str, data: dict):
    volume_m = data['volume'] * data['close'] / 1_000_000
    interval = data.get('interval', '?')
    text = (
        f"🟡 WHALE PUMP SIGNAL\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"Coin     : {symbol}\n"
        f"Timeframe: {interval}\n"
        f"Narx     : ${data['close']:,.4f}\n"
        f"Hajm     : ${volume_m:.1f}M\n"
        f"WP       : {data['whale_pump']}\n"
        f"KDJ-K    : {data['K']}\n"
        f"KDJ-D    : {data['D']}\n"
        f"KDJ-J    : {data['J']}\n"
        f"Vaqt     : {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"Birja    : Binance SPOT"
    )
    await bot.send_message(chat_id=int(TELEGRAM_CHAT_ID), text=text)

async def send_status(msg: str):
    await bot.send_message(chat_id=int(TELEGRAM_CHAT_ID), text=msg)
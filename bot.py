import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = 7637741947:AAFMq4UMrxUfyoMYGIyPh0tvvRfVzYs3upQ
ADMIN_ID = 6920665561

bot = Bot(token=TOKEN)
dp = Dispatcher()

db = sqlite3.connect("films.db")
sql = db.cursor()

sql.execute("""
CREATE TABLE IF NOT EXISTS films (
    code TEXT PRIMARY KEY,
    title TEXT,
    watch TEXT,
    download TEXT
)
""")
db.commit()

def film_keyboard(watch, download):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="▶️ Смотреть", url=watch),
            InlineKeyboardButton(text="⬇️ Скачать", url=download)
        ]
    ])

@dp.message()
async def handler(message: types.Message):
    text = message.text.strip()

    if text.startswith("+") and message.from_user.id == ADMIN_ID:
        try:
            data = text[1:].split("|")
            code = data[0].strip().upper()
            title = data[1].strip()
            watch = data[2].strip()
            download = data[3].strip()

            sql.execute(
                "INSERT OR REPLACE INTO films VALUES (?, ?, ?, ?)",
                (code, title, watch, download)
            )
            db.commit()

            await message.answer(f"✅ Фильм добавлен:\n{code} — {title}")
        except:
            await message.answer(
                "❌ Ошибка формата\n"
                "+КОД | Название | ссылка_смотреть | ссылка_скачать"
            )
        return

    code = text.upper()
    sql.execute("SELECT title, watch, download FROM films WHERE code = ?", (code,))
    film = sql.fetchone()

    if film:
        title, watch, download = film
        await message.answer(
            f"🎬 <b>{title}</b>\nКод: <code>{code}</code>",
            reply_markup=film_keyboard(watch, download),
            parse_mode="HTML"
        )

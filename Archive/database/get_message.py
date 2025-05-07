import aiosqlite
import aiogram
from config import *
from aiogram import Bot

bot = Bot(TOKEN)


async def get_message(
    chat_id: int
):
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM data") as cur:
            fetch = await cur.fetchone()
            print(fetch)
        async with db.execute("SELECT * FROM data WHERE chat_id = ?", (chat_id,)) as cursor:
            fetch = await cursor.fetchone()
    if fetch is None:
        return None

    return fetch[0]


async def edit_message(
    chat_id,
    text,
    reply_markup=None
):

    message_id = await get_message(chat_id)
    print(message_id)
    print(chat_id)
    await bot.edit_message_text(
        chat_id=chat_id,
        text=text,
        message_id=message_id,
        reply_markup=reply_markup
    )
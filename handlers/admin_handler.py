from aiogram.filters import Command
from aiogram import Router, F, types
from config import *
from filters.admin import Admin
import aiosqlite

router = Router()

@router.message(Command("ap"), Admin())
async def apanel(
    message: types.Message
):
    await message.answer("""
    Команды для администрирования:
    • /send ТЕКСТ - рассылает текст всем пользователям бота
    """)

@router.message(Command("send"), Admin())
async def send(
    message: types.Message
):
    if " " not in message.text:
        await message.answer("Введите текст для рассылки в виде аргумента")
        return

    text = message.text.split(" ")[1]

    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            fetch = await cursor.fetchall()

    for user in fetch:
        user_id = user[0]
        await bot.send_message(
            chat_id=user_id,
            text=text
        )

    await message.answer("Рассылка завершена.")




    
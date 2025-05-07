from aiogram import Bot, F, Router
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from config import *
from aiogram.filters import Command
from keyboards.inline import *
from datetime import datetime
import aiosqlite

router = Router()

bot = Bot(TOKEN)

@router.message(F.text, Command("start"))
async def start(
    message: types.Message
):
    check_member = True	
    member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
    if member.status == "left":
        check_member = False
    if not check_member:
        url = InlineKeyboardBuilder()
        url.button(
            text="✅Подписаться",
            url=CHANNEL_LINK
        )
        url.button(
            text="✅Подписаться",
            url="https://t.me/m3ka3"
        )
        url.button(
            text="✅Я подписался!",
            callback_data="check_subscription"
       )
	
        await message.answer("🕸️Вы не подписаны на каналы, подпишитесь, чтоб пользоваться функциями бота!", reply_markup=url.as_markup())
        return
    username = message.from_user.full_name
    username = username.replace("<", "")
    username = username.replace(">", "")

    async with aiosqlite.connect("users.db") as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id, username, date_registration) VALUES (?, ?, ?)", (message.from_user.id, username, datetime.now()))
        await db.commit()
    await message.answer(
        text="🔎Чтобы найти музыку, введите <b>имя исполнителя или название песни.</b>",
        reply_markup=menu()
    )
    
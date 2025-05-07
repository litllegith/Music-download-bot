from aiogram import Bot, F, Router
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from config import *

router = Router()

bot = Bot(TOKEN)

@router.message()
async def check_sub(
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
			text="✅Я подписался!",
			callback_data="check_subscription"
		)
	
		await message.answer("🕸️Вы не подписаны на каналы, подпишитесь, чтоб пользоваться функциями бота!", reply_markup=url.as_markup())
		return
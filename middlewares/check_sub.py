from aiogram import Router, types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.exceptions import TelegramAPIError
from aiogram import Bot
from config import * 

class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def __call__(self, handler, event, data):
        # Пропускаем служебные апдейты и команду /start
        if not isinstance(event, types.Message) or event.text == "/start":
            return await handler(event, data)

        user_id = event.from_user.id
        try:
            member = await self.bot.get_chat_member(CHANNEL_ID, user_id)
            if member.status in ["member", "administrator", "creator"]:
                return await handler(event, data)
        except TelegramAPIError as e:
            print(f"Ошибка проверки подписки: {e}")
            return await handler(event, data)

        # Если не подписан - отправляем сообщение с кнопкой
        markup = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(
                text=BUTTON_TEXT,
                url=f"https://t.me/{YOUR_CHANNEL_USERNAME}")]  # Юзернейм канала
        ])

        await event.answer(
            text=SUBSCRIBE_TEXT,
            reply_markup=markup,
            parse_mode="HTML"
        )

        # Прерываем дальнейшую обработку
        return

# Подключение middleware

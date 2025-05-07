from aiogram.filters import BaseFilter
from config import ADMIN_ID
from aiogram import types

class Admin(
    BaseFilter
):
    """Фильтр админов в боте, админы указываются в конфиге в поле ADMIN_ID"""
    def __init__(
        self
    ):
        pass

    async def __call__(
        self,
        message: types.Message
    ):
        return message.from_user.id in ADMIN_ID

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from handlers import start, callbacks, admin_handler, check_sub
from config import *
import logging
import asyncio
import sqlite3

logging.basicConfig(level=logging.INFO)

bot = Bot(
     token=TOKEN,
     default=DefaultBotProperties(
         parse_mode=ParseMode.HTML))

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

conn = sqlite3.connect("users.db")

cursor = conn.cursor()

cursor.execute("""
	CREATE TABLE IF NOT EXISTS users(
		user_id INTEGER UNIQUE,
		username TEXT,
		date_registration TEXT
		)"""
	)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS data(
        message_id INTEGER UNIQUE,
        chat_id INTEGER UNIQUE
        )"""
    )

conn.commit()
conn.close()


async def main():
	dp.include_routers(
        start.router,
        admin_handler.router,
        callbacks.router
    )

	await dp.start_polling(bot)
	
	
if __name__ == "__main__":
	asyncio.run(main())
import asyncio
import logging
import os

import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s : %(levelname)s : %(message)s"
)

load_dotenv()

TOKEN = os.getenv("TOKEN")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
if not TOKEN:
    raise ValueError("Токен не найден!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.info("Бот запускается...")


async def create_db_pool():
    return await asyncpg.create_pool(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT
    )


@dp.message(CommandStart())
async def start(message: types.Message):
    logging.info(f"Получена команда start")
    await message.reply('Вы нажали команду старт ;)')


@dp.message(Command('help'))
async def help(message: types.Message):
    logging.info("Получена команда help")
    await message.reply('Пока что ничем не могу вам помочь)')


@dp.message()
async def echo(message: types.Message):
    logging.info(f"Получено что-то от {message.from_user.id}: {message.text}")
    await message.reply(f'Зачем мне информация {message.text}')


async def main() -> None:

    db_pool = await create_db_pool()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.info("Бот запущен")
        asyncio.run(main())

    except Exception as ex:
        logging.error(f"ОШИБИЩЕ {ex}")


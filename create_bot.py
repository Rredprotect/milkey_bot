import asyncio
import logging
import os
from datetime import datetime
import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s : %(levelname)s : %(message)s"
)

load_dotenv()
db_pool = None

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
    await log_user_request(message)
    await message.reply('Вы нажали команду старт ;)')


@dp.message(Command('help'))
async def help(message: types.Message):
    logging.info("Получена команда help")
    await log_user_request(message)
    await message.reply('Пока что ничем не могу вам помочь)')

@dp.message(Command('dump'))
async def dump(message: types.Message):
    await get_info(message)


@dp.message()
async def echo(message: types.Message):
    await log_user_request(message)
    logging.info(f"Получено что-то от {message.from_user.id}: {message.text}")
    await message.reply(f'Зачем мне информация {message.text}')

async def log_user_request(message: types.Message):
    try:
        async with db_pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO users(user_id, username, request_time)
                VALUES($1, $2, $3)
            ''', message.from_user.id, message.from_user.username, datetime.now())
        logging.info("Данные успешно записаны!")
    except Exception as ex:
        logging.error(f"Ошибка при записи данных в бд {ex}")

async def get_info(message: types.Message):
    try:
        async with db_pool.acquire() as conn:
            rows  = await conn.fetch('SELECT user_id, username, request_time FROM users ORDER BY request_time DESC LIMIT 5')
            response = "Последнии 5 записей:\n"
            for row in rows:
                response += f"User ID : {row["user_id"]},   Username: {row["username"]},   Time: {row["request_time"]}\n"
            await message.answer(response)
    except Exception as ex:
        logging.error(f"Ошибка при получении данных из бд: {ex}")


async def main() -> None:
    global db_pool
    db_pool = await create_db_pool()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.info("Бот запущен")
        asyncio.run(main())

    except Exception as ex:
        logging.error(f"ОШИБИЩЕ {ex}")


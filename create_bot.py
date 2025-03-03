import asyncio
import logging
import os
from datetime import datetime
import asyncpg
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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

keyboard = ReplyKeyboardBuilder()
keyboard.button(text="but1")
keyboard.button(text="Умножить числа")
keyboard.adjust(2)
keyboard_but = keyboard.as_markup(resize_keyboard=True)

user_data = {}



@dp.message(Command('start'))
async def start(message: types.Message):
    logging.info(f"Получена команда start")
    await log_user_request(message)
    await message.reply('Вы нажали команду старт ;)', reply_markup=keyboard_but)

@dp.message(F.text == "but1")
async def handler_but1(message: Message):
    await message.answer("we well rock you ")

@dp.message(Command('help'))
async def help(message: types.Message):
    logging.info("Получена команда help")
    await log_user_request(message)
    await message.reply('Пока что ничем не могу вам помочь)')

@dp.message(Command('dump'))
async def dump(message: types.Message):
    await get_info(message)

@dp.message(F.text == "Умножить числа")
async def handle_multiply_button(message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {}  # Создаём запись для пользователя
    await message.answer("Введите первое число:")


@dp.message(F.text)
async def handle_numbers(message: Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        await message.answer("Нажмите 'Умножить числа', чтобы начать.")
        return

    if "first_number" not in user_data[user_id]:
        try:
            first_number = float(message.text)
            user_data[user_id]["first_number"] = first_number
            await message.answer("Введите второе число:")
        except ValueError:
            await message.answer("Пожалуйста, введите корректное число.")
    else:
        try:
            second_number = int(message.text)
            first_number = int(user_data[user_id]["first_number"])
            result = first_number * second_number
            await message.answer(f"Результат умножения {first_number} и {second_number} равен {result}.")
            user_data.pop(user_id)
        except ValueError:
            await message.answer("Пожалуйста, введите корректное число.")

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


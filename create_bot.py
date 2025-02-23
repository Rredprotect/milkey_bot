import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s : %(levelname)s : %(message)s"
)

load_dotenv()

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("Токен не найден!")


dp = Dispatcher()

logging.info("Бот запускается...")


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
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN)

    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
        logging.info("Бот запущен")
        # async start_polling(dp, skip_updates=True)
    except Exception as ex:
        logging.error(f"ОШИБИЩЕ {ex}")


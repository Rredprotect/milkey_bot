import asyncio
import logging
from bot.core.config import Config
from bot.core.bot import dp, bot
from bot.database.connection import create_db_pool
from bot.handlers import commands, messages
from bot.handlers.errors import router as errors_router


async def main():
    # Валидация конфигурации
    Config.validate()

    # Инициализация БД
    pool = await create_db_pool()

    dp.include_router(commands.router)
    dp.include_router(messages.router)
    dp.include_router(errors_router)

    # Запуск бота
    try:
        await dp.start_polling(bot)
    finally:
        await pool.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
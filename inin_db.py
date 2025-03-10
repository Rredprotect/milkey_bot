import asyncio
import logging
from bot.database.setup import create_tables

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(create_tables())
    print("✅ База данных успешно инициализирована")
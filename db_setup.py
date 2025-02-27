import asyncpg
import asyncio
from dotenv import load_dotenv
import os
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s : %(levelname)s : %(message)s"
)

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

if not all([DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT]):
    raise ValueError("Некоторые параметры для подключения к бд не найдены")


async def create_db():
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT
    )

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        username VARCHAR(100),
        request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    await conn.close()
    logging.info('Таблица создана')

if __name__ == "__main__":
    asyncio.run(create_db())
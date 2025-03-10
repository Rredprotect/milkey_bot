import asyncpg
import logging
import asyncio
from ..core.config import Config

async def create_tables():
    try:
        conn = await asyncpg.connect(**Config.DB_CONFIG)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                username VARCHAR(100),
                request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        logging.info("Таблицы успешно созданы")
    except Exception as e:
        logging.error(f"Ошибка при создании таблиц: {e}")
        raise
    finally:
        await conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(create_tables())
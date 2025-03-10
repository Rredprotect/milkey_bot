from datetime import datetime
import logging
from .connection import create_db_pool

async def log_user_request(user_id: int, username: str):
    try:
        logging.debug(f"[DEBUG] Params types - user_id: {type(user_id)}, username: {type(username)}")
        logging.debug(f"[DEBUG] username value: {repr(username)}")
        pool = await create_db_pool()
        async with pool.acquire() as conn:
            # crud.py
            await conn.execute('''
                INSERT INTO users(user_id, username, request_time)
                VALUES($1, $2::VARCHAR, $3)
            ''', user_id, username, datetime.now())  # Явное приведение типа
    except Exception as ex:
        logging.error(f"Ошибка БД: {ex}")


    try:
        pool = await create_db_pool()
        if not pool:
            raise Exception("Пустое подключение к БД")
        async with pool.acquire() as conn:
            await conn.execute(...)
    except Exception as ex:
        logging.error(f"Ошибка БД: {ex}")
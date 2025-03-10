import asyncpg
from ..core.config import Config



async def create_db_pool():
    return await asyncpg.create_pool(**Config.DB_CONFIG)
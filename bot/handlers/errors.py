import logging
from aiogram import Router
from aiogram.types import ErrorEvent

router = Router()

@router.errors()
async def error_handler(event: ErrorEvent):
    logging.critical("Критическая ошибка!", exc_info=event.exception)
    return True

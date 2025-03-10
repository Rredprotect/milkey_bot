from aiogram import types
from aiogram.filters import Command
from milkey_bot.bot.core.bot import dp, bot
from milkey_bot.bot.database.crud import log_user_request
import logging
from aiogram import Router
router = Router()

@router.message(Command('start'))
async def start_handler(message: types.Message):
    user = message.from_user
    username = user.username if user.username is not None else ""
    await log_user_request(user.id, username)
    await message.reply(f"Привет, {user.first_name}! Я бот-пример.")
    logging.info(f"Новый пользователь: {username}")

@router.message(Command('help'))
async def help_handler(message: types.Message):
    await message.reply("Доступные команды:\n/start - начать работу\n/help - помощь")
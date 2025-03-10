from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from .config  import Config

bot = Bot(token=Config.TOKEN)
dp = Dispatcher()
user_data = {}
from aiogram import F, types
from milkey_bot.bot.core.bot import dp, user_data
from aiogram import Router
router = Router()


@router.message(F.text == "Умножить числа")
async def multiply_start(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    await message.answer("Введите первое число:")

@router.message(F.text)
async def process_numbers(message: types.Message):
    user_id = message.from_user.id
    # ... (ваша логика обработки чисел)
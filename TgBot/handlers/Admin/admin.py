from aiogram import types, Dispatcher
from config import dp, ADMINS
from keyboards import admin_kb


@dp.message_handler(commands=["admin"])
async def admin_handler(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer("Что хозяин надо????", reply_markup=admin_kb.main_panel())


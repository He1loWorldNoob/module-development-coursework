from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from config import dp, ADMINS
from data_base import sqlite_db


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('del_'))
async def del_callback_run(callback: CallbackQuery):
    data = callback.data.split("_")
    sqlite_db.remove_product(data[1])

    await callback.message.edit_text("Удалено")

@dp.message_handler(lambda message: 'Удалить товар' in message.text)
async def delt_handler(message: types.Message):
    if message.from_user.id in ADMINS:
        products = sqlite_db.get_all_products()

        if not products:
            await message.answer("Нет товаров для удаления.")
            return

        for product in products:

            kb = InlineKeyboardMarkup().add(
                InlineKeyboardButton(f"Удалить {product[1]}", callback_data=f"del_{product[0]}_{product[1]}")
            )

            caption = (
                f"ID: {product[0]}\n"
                f"Название: {product[1]}\n"
                f"Тип: {product[2]}\n"
                f"Описание: {product[3]}\n"
                f"Цена: {product[5]}₽"
            )


            await message.reply_photo(
                photo=product[4],
                caption=caption,
                reply_markup=kb
            )

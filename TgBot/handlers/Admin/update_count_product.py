from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text



from config import dp, ADMINS
from data_base import sqlite_db
from keyboards import admin_kb


class FSMUpdateCount(StatesGroup):
    choosing = State()
    entering = State()


@dp.message_handler(lambda message: 'Обновить количество' in message.text)
async def start_update(message: types.Message):
    if message.from_user.id not in ADMINS:
        return

    await message.answer("Выберете какой товар обновить.", reply_markup=admin_kb.admin_cancel())

    products = sqlite_db.get_all_products()

    if not products:
        await message.answer("Нет товаров для обновления.")
        return

    for product in products:
        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton(f"Изменить количество", callback_data=f"upd_{product[0]}")
        )
        caption = (
            f"{product[1]}\n"
            f"Тип: {product[2]}\n"
            f"Описание: {product[3]}\n"
            f"Цена: {product[5]}₽\n"
            f"В наличии: {product[6]}"
        )

        await message.answer_photo(
            photo=product[4],
            caption=caption,
            reply_markup=kb
        )

    await FSMUpdateCount.choosing.set()

@dp.message_handler(Text(equals='Отменить', ignore_case=True), state=FSMUpdateCount)
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await state.finish()
        await message.reply('Обновление отменено', reply_markup = admin_kb.main_panel())

@dp.callback_query_handler(lambda c: c.data.startswith('upd_'), state=FSMUpdateCount.choosing)
async def product_chosen(callback: types.CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split('_')[1])

    async with state.proxy() as data:
        data['product_id'] = product_id

    await callback.message.answer("Введите новое количество товара (целое число):")
    await FSMUpdateCount.entering.set()


@dp.message_handler(state=FSMUpdateCount.entering)
async def set_new_count(message: types.Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("Введите целое число!")
        return

    async with state.proxy() as data:
        product_id = data['product_id']
        new_count = int(message.text)

    sqlite_db.update_product_count(product_id, new_count)

    await message.answer(f"Количество товара обновлено: теперь {new_count} шт.", reply_markup=admin_kb.main_panel())
    await state.finish()

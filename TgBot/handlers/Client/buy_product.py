from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from config import bot, ADMINS, dp
from data_base import sqlite_db
from keyboards import common_kb, client_kb

import re
from datetime import datetime

class FSMBuy(StatesGroup):
    product_type = State()
    product = State()
    name = State()
    time = State()
    address = State()
    telephone = State()
    confirm = State()



@dp.message_handler(lambda message: 'Оформить заказ' in message.text)
async def start_buy(message: types.Message):
    await message.answer('Выберите тип товара', reply_markup=common_kb.product_type())
    await FSMBuy.product_type.set()



@dp.message_handler(Text(equals='Отменить', ignore_case=True), state=FSMBuy)
@dp.message_handler(Text(equals='Отменить', ignore_case=True), state=None)
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Покупка отменена", reply_markup=client_kb.start(message.from_user.id))



@dp.message_handler(state=FSMBuy.product_type)
async def product_type(message: types.Message, state: FSMContext):
    products = sqlite_db.get_available_products_by_type(message.text)

    if not products:
        await message.answer("В данной категории нет товаров.", reply_markup=common_kb.product_type())
        return

    for product in products:

        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton(f"Выбрать {product[1]}", callback_data=f"ch_{product[0]}_{product[1]}")
        )
        await message.answer("Выберете что хотите.", reply_markup= common_kb.cancel())
        caption = (
            f"Название: {product[1]}\n"
            f"Тип: {product[2]}\n"
            f"Описание: {product[3]}\n"
            f"Цена: {product[5]}₽"
        )

        await message.answer_photo(
            photo=product[4],
            caption=caption,
            reply_markup=kb
        )

    # Переходим на выбор конкретного товара
    await FSMBuy.product.set()


@dp.callback_query_handler(lambda c: c.data.startswith('ch_'), state=FSMBuy.product)
async def choice_product(callback: types.CallbackQuery, state: FSMContext):

    data = callback.data.split("_")

    product_id = data[1]
    product_data = sqlite_db.get_product_by_id(product_id)

    if not product_data:
        await callback.message.answer("Не удалось найти товар.")
        return


    async with state.proxy() as state_data:
        state_data['product'] = product_data[0]


    user_id = callback.message.from_user.id
    print(user_id)

    await callback.message.answer("Как к вам обращаться?")

    await FSMBuy.name.set()


@dp.message_handler(state=FSMBuy.name)
async def set_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer("Введите адрес доставки\nПример: Малышева 1")
    await FSMBuy.address.set()

@dp.message_handler(state=FSMBuy.address)
async def set_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text

    await message.answer("Введите желаемую дату и время доставки\nПример: 14:30")
    await FSMBuy.time.set()


@dp.message_handler(state=FSMBuy.time)
async def set_time(message: types.Message, state: FSMContext):
    time_str = message.text.strip()

    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        await message.answer("Некорректный формат времени.\nПример: 14:30")
        return

    async with state.proxy() as data:
        data['time'] = time_str

    await message.answer("Введите номер телефона по которому с вами можно связаться\nПример: +79123456789")
    await FSMBuy.telephone.set()



@dp.message_handler(state=FSMBuy.telephone)
async def set_telephone(message: types.Message, state: FSMContext):
    phone = message.text.strip()

    if not re.fullmatch(r"\+7\d{10}", phone):
        await message.answer("Некорректный номер телефона.\nПример: +79123456789")
        return

    async with state.proxy() as data:
        data['telephone'] = phone
        product = data['product']

        text = (
            f"Подтвердите заказ:\n"
            f"TG: @{message.from_user.username}\n"
            f"Товар: {product[1]}\n"
            f"Описание: {product[3]}\n"
            f"Цена: {product[5]}₽\n\n"
            f"Имя: {data['name']}\n"
            f"Адрес: {data['address']}\n"
            f"Время: {data['time']}\n"
            f"Телефон: {data['telephone']}"
        )

        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Подтвердить", callback_data="confirm_order"),
            InlineKeyboardButton("Отменить", callback_data="cancel_order")
        )

        await message.answer(text, reply_markup=kb)
        await FSMBuy.confirm.set()



@dp.callback_query_handler(lambda c: c.data == "confirm_order", state=FSMBuy.confirm)
async def confirm_order(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        product = data['product']

        order_text = (
            f"Новый заказ!\n\n"
            f"TG: @{callback.from_user.username}\n"
            f"Товар: {product[1]}\n"
            f"Описание: {product[3]}\n"
            f"Цена: {product[5]}₽\n\n"
            f"Имя: {data['name']}\n"
            f"Адрес: {data['address']}\n"
            f"Время: {data['time']}\n"
            f"Телефон: {data['telephone']}"
        )

        sell_id = sqlite_db.add_sell(data, callback.from_user, product[0])
        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Подтвердить заказ",
                                 callback_data=f"accept_manager_{sell_id}_{callback.from_user.id}"),
            InlineKeyboardButton("Отменить заказ", callback_data=f"cancel_manager_{sell_id}_{callback.from_user.id}")
        )

        for admin_id in ADMINS:
            await bot.send_message(admin_id, order_text, reply_markup=kb)

        await callback.message.edit_text("Заказ оформлен! Ожидайте, с вами свяжется менеджер.")
        await callback.message.answer("Вы вернулись в главное меню", reply_markup=client_kb.start(callback.from_user.id))
        await state.finish()








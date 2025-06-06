from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMINS, dp, bot
from data_base import sqlite_db
from keyboards import admin_kb, common_kb


class FSMAddProduct(StatesGroup):
    name = State()
    product_type = State()
    photo = State()
    description = State()
    price = State()
    count = State()
    confirm = State()



@dp.message_handler(lambda message: 'Добавить товар' in message.text)
async def start_add_product(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.reply('Название товара', reply_markup=admin_kb.admin_cancel())
        await FSMAddProduct.name.set()


@dp.message_handler(Text(equals='Отменить', ignore_case=True), state=FSMAddProduct)
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await state.finish()
        await message.reply('Добавление отменено', reply_markup = admin_kb.main_panel())


@dp.message_handler(state=FSMAddProduct.name)
async def set_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('Выберите тип', reply_markup = common_kb.product_type())
    await FSMAddProduct.product_type.set()

@dp.message_handler(state=FSMAddProduct.product_type)
async def set_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_type'] = message.text

    await message.reply('Отправьте фото', reply_markup=admin_kb.admin_cancel())
    await FSMAddProduct.photo.set()


@dp.message_handler(content_types=['photo'], state=FSMAddProduct.photo)
async def set_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await message.reply('Теперь введите описание', reply_markup=admin_kb.admin_cancel())
    await FSMAddProduct.description.set()


@dp.message_handler(state=FSMAddProduct.description)
async def set_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await message.reply('Теперь укажите цену', reply_markup=admin_kb.admin_cancel())
    await FSMAddProduct.price.set()


@dp.message_handler(state=FSMAddProduct.price)
async def set_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not message.text.isdigit():
            await message.answer("Введите число для цены!")
            return
        data['price'] = int(message.text)


    await message.answer("Введите количество товара на складе:", reply_markup=admin_kb.admin_cancel())
    await FSMAddProduct.count.set()




@dp.message_handler(state=FSMAddProduct.count)
async def set_count(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите целое число!")
        return


    async with state.proxy() as data:
        data['count'] = message.text

        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text="Подтвердить", callback_data="confirm_add"),
            InlineKeyboardButton(text="Отменить", callback_data="cancel_add")
        )

        await message.answer_photo(
            photo=data['photo'],
            caption=(
                f"Название: {data['name']}\n"
                f"Тип: {data['product_type']}\n"
                f"Описание: {data['description']}\n"
                f"Цена: {data['price']}₽\n"
                f"Количество: {data['count']}"
            ),
            reply_markup=kb
        )

    await FSMAddProduct.confirm.set()



@dp.callback_query_handler(lambda c: c.data == 'confirm_add', state=FSMAddProduct.confirm)
async def confirm_product(callback: types.CallbackQuery, state: FSMContext):

    try:

        async with state.proxy() as data:
            sqlite_db.add_product(data)
            await callback.message.edit_caption(f'Товар "{data["name"]}" добавлен')
    except Exception as e:
        print(e)


    await callback.message.answer("Товар добавлен.", reply_markup=admin_kb.main_panel())
    #await bot.send_message(callback.from_user.id, "Товар добавлен", reply_markup=admin_kb.main_panel())
    await state.finish()




@dp.callback_query_handler(lambda c: c.data == 'cancel_add', state=FSMAddProduct.confirm)
async def cancel_product(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await callback.message.edit_caption(f'Товар "{data["name"]}" добавлен')
    await bot.send_message(callback.from_user.id, "Добавление отменено", reply_markup=admin_kb.main_panel())
    await state.finish()















from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import dp
from data_base import sqlite_db
from keyboards import client_kb


class FSMReview(StatesGroup):
    review = State()

@dp.callback_query_handler(lambda c: c.data.startswith('review_'))
async def delivered_waiting(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split("_")
    sell_id = data[1]

    async with state.proxy() as data:
        data['sell_id'] = sell_id

    await FSMReview.review.set()
    await callback.message.edit_text("Напишите свой отзыв")






@dp.message_handler(state= FSMReview.review)
async def review(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        sell_id = data.get('sell_id')
        sqlite_db.update_sell_review(sell_id, message.text)
    print(f"Отзыв по заказу {sell_id}: {message.text}")

    await message.answer("Спасибо за оставленный отзыв",reply_markup=client_kb.start(message.from_user.id))
    await state.finish()
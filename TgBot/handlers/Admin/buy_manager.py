from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import bot, dp
from data_base import sqlite_db
from keyboards import client_kb


@dp.callback_query_handler(lambda c: c.data.startswith('accept_manager_'))
async def order_accepted(callback: types.CallbackQuery):
    data = callback.data.split("_")
    sell_id = data[2]
    client_id = data[3]
    manager = callback.from_user.username

    await bot.send_message(client_id, f"Ваш заказ принял менеджер @{manager}")

    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Жду клиента", callback_data=f"delivered_waiting_{sell_id}_{client_id}"),
        InlineKeyboardButton("Заказ доставлен", callback_data=f"delivered_accept_{sell_id}_{client_id}"),
    )
    await callback.message.edit_reply_markup(kb)

    sqlite_db.update_sell_status(sell_id, "delivered")



@dp.callback_query_handler(lambda c: c.data.startswith('cancel_manager_'))
async def cancel_order(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split("_")
    sell_id = data[2]
    client_id = data[3]


    reply_markup = client_kb.start(client_id)
    await bot.send_message(client_id, f"Заказ отменён менеджером @{callback.from_user.username}", reply_markup=reply_markup)

    sqlite_db.update_sell_status(sell_id, "cancel")





@dp.callback_query_handler(lambda c: c.data.startswith('delivered_accept_'))
async def delivered_accept(callback: types.CallbackQuery):
    data = callback.data.split("_")
    sell_id = int(data[2])
    client_id = int(data[3])

    sqlite_db.update_sell_status(sell_id, "ended")

    product_id = sqlite_db.get_product_id_by_sell(sell_id)

    if product_id:
        sqlite_db.decrease_product_count(product_id)

    await callback.message.delete()

    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Отзыв", callback_data=f"review_{sell_id}"),
    )
    await bot.send_message(client_id, "Спасибо за заказ, оставьте пожалуйста отзыв что бы помочь нам стать лучше :)", reply_markup=kb)



@dp.callback_query_handler(lambda c: c.data.startswith('delivered_waiting_'))
async def delivered_waiting(callback: types.CallbackQuery):
    data = callback.data.split("_")
    sell_id = data[2]
    client_id = data[3]

    await bot.send_message(client_id, f"Вас ожидает курьер")
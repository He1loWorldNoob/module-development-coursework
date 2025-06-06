from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btn_add_product = KeyboardButton("Добавить товар")
btn_delete_product = KeyboardButton("Удалить товар")
btn_update_count_product = KeyboardButton("Обновить количество")

btn_back_to_main = KeyboardButton("В главное меню")
btn_cancel = KeyboardButton("Отменить")


def main_panel():
    return (
        ReplyKeyboardMarkup(resize_keyboard=True)
        .add(btn_add_product)
        .insert(btn_delete_product)
        .insert(btn_update_count_product)
        .add(btn_back_to_main)
    )


def admin_cancel():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel)


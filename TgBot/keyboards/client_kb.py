from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMINS

# Кнопки
order_btn = KeyboardButton('Оформить заказ')
help_btn = KeyboardButton('Помощь')
info_btn = KeyboardButton('Информация')



confirm_btn = KeyboardButton('Подтвердить')
repeat_btn = KeyboardButton('Повторить заказ')
main_menu_btn = KeyboardButton('Главное меню')
cancel_btn = KeyboardButton('Отменить')

admin_button = KeyboardButton("/admin")

def start(userId):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(order_btn).add(info_btn).insert(help_btn)
    if userId in ADMINS:
        kb.add(admin_button)
    return kb



def choice_taste(list_taste) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    for taste in list_taste:
        ikb.add(InlineKeyboardButton(text=taste, callback_data=f'tst_{taste}'))
    return ikb

def apply():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(confirm_btn).add(cancel_btn)
    return kb

def cancel():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(cancel_btn)

def repeat_or_main():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(repeat_btn).add(main_menu_btn)
    return kb

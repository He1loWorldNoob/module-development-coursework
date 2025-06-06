from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

snus_btn = KeyboardButton('Снюс')
liquid_btn = KeyboardButton('Жидкость')
one_sides_btn = KeyboardButton('Одноразка')

cancel_btn = KeyboardButton('Отменить')

def cancel():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(cancel_btn)

def product_type():
    return (ReplyKeyboardMarkup(resize_keyboard=True).insert(liquid_btn)
            .insert(snus_btn)
            .insert(one_sides_btn)
            .add(cancel_btn))


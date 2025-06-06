from aiogram import types
from config import dp
from keyboards import client_kb


start_command = '''What`s up дружище 🤙
Я бот Антоша, в этом разделе я собрал для тебя всë необходимое:
/start'''

@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await message.answer(start_command, reply_markup=client_kb.start(message.from_user.id))
    await message.delete()


@dp.message_handler(lambda message: 'В главное меню' in message.text)
async def process_help_command(message: types.Message):
    await message.answer("Главное меню",reply_markup=client_kb.start(message.from_user.id))
    await message.delete()


rules_command = '''🔥free shipping🔥
Бесплатная доставка 
   доступна каждому гостю, при заказе от любой суммы.
(https://t.me/G13_Shop_bot) 
Закажи легко и просто, жми кнопку "Оформить заказ" в главном меню, далее тебе поможет Антоша 

🕙Время работы доставки🕣
                 10:00-20:00'''

@dp.message_handler(commands=["rule"])
@dp.message_handler(lambda message: 'Информация' in message.text)
async def process_help_command(message: types.Message):
    await message.answer(rules_command,reply_markup=client_kb.start(message.from_user.id))
    await message.delete()

help_command = """
По всем вопросам и
предложениям:
👻@G13_Manager
"""
@dp.message_handler(commands=["help"])
@dp.message_handler(lambda message: 'Помощь' in message.text)
async def process_help_command(message: types.Message):
    await message.answer(help_command,reply_markup=client_kb.start(message.from_user.id))
    await message.delete()

@dp.message_handler()
async def empty(message: types.Message):
    await message.answer('Нет такой команды')
    await message.delete()
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

TOKEN = '6384105446:AAG_ef4dxCYDdVqE1VKDf8IkFQ-_UcHMMqk'

bot = Bot(token=TOKEN)

dp = Dispatcher(bot, storage=storage)

admin_g13_danil = 2054779185

ADMINS = (admin_g13_danil,)



from aiogram.utils import executor

from config import dp, bot
from data_base import sqlite_db
from handlers import common


async  def on_startup(_):
    sqlite_db.sql_start()
    info = await bot.get_webhook_info()
    print(f'Bot online {info}')

if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, allowed_updates=["message", "inline_query", "callback_query"])

from aiogram import executor
import logging
from handlers import users_h, admin_add_file, admin_del_file, admin_add_category, admin_del_category
from client import dp
from sqlite_db import AdminDATA

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print("Бот вышел в сеть!")
    AdminDATA.sql_start()

users_h.register_handlers_users(dp)
admin_add_file.register_handlers_admin(dp)
admin_del_file.register_handlers_admin(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

from aiogram import executor
import logging
from handlers import users_h, help_h
from handlers.admin_handlers import admin_add_file, admin_del_file, admin_add_category, admin_del_category
from Test_photo import test_photo_h
from client import dp, bot
from sqlite_db import AdminDATA

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print("Бот вышел в сеть!")
    AdminDATA.sql_start()
    # all_users = AdminDATA.get_all_user_id()
    # for i in all_users:
    #     await bot.send_message(
    #         i[0], "<strong>Бот был перезагружен с целью обновления функционала и редактирования категорий</strong> \n\n<b>Пожалуйста, пропишите /start для исключения ошибок работы функций бота!</b> \n\n<i>Подробнее об обновлении или поплнении Вы можете узнать в канале</i> <a href='t.me/os_store_update'>OS_Store update</a>", parse_mode='HTML')


test_photo_h.register_test_photo(dp)
admin_add_file.register_handlers_admin(dp)
admin_del_file.register_handlers_admin(dp)
admin_add_category.register_handlers_add_cat(dp)
admin_del_category.register_handlers_del_cat(dp)
users_h.register_handlers_users(dp)
help_h.register_message_help(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

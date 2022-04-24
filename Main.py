from aiogram import executor
import logging
from handlers import users_h, help_h, buy, qiwi, FAQ_h
from handlers.admin_handlers import (
    admin_add_file,
    admin_del_file,
    admin_add_category,
    admin_del_category,
    admin_commad,
)
from Test_photo import test_photo_h
from client import dp, bot
from sqlite_db import AdminDATA

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    all_users = AdminDATA.get_all_user_id()
    for i in all_users:
        await bot.send_message(
            i[0],
            "<b>Бот был перезагружен с целью обновления функционала и редактирования категорий</b> \n\n<b>Пожалуйста, пропишите /start для исключения ошибок работы функций бота!</b> \n\n<i>Подробнее об обновлении или поплнении Вы можете узнать в канале</i> <a href='t.me/os_store_update'>OS Store ОБНОВЛЕНИЯ</a>",
            parse_mode="HTML",
        )


FAQ_h.register_FAQ_information(dp)
qiwi.register_buy_handler(dp)
buy.register_pay_handler(dp)
test_photo_h.register_test_photo(dp)
admin_commad.register_admin_command_handler(dp)
admin_add_file.register_handlers_admin(dp)
admin_del_file.register_handlers_admin(dp)
admin_add_category.register_handlers_add_cat(dp)
admin_del_category.register_handlers_del_cat(dp)
users_h.register_handlers_users(dp)
help_h.register_message_help(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

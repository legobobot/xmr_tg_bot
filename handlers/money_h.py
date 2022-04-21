from aiogram import Dispatcher, types
from sqlite_db import UserDB as user
import Keyboard as key
from client import bot
from sqlite_db import main_data as data
from sqlite_db import moneyDB as money


async def my_shop(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, "Ваши покупки!")


def register_new_referal(dp: Dispatcher):
    dp.register_callback_query_handler(my_shop, text='my_shop')

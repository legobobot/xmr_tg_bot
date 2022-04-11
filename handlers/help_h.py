from aiogram import Dispatcher, types
from Db import Database as data
from UsersDB import Users as User
import Keyboard as key
from client import bot
from sqlite_db import main_data as mdata


async def help(message: types.Message):
    await message.answer("Вы перешли в меню помощи пользователям!\nЧто вы хотите сделать?", reply_markup=key.help)


def register_message_help(dp: Dispatcher):
    dp.register_message_handler(help, text="Помощь")

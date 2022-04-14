from aiogram import Dispatcher, types
import sqlite_db.UserDB as user
import Keyboard as key
from client import bot
from sqlite_db import main_data as main_data


async def help(message: types.Message):
    await message.answer("Вы перешли в меню помощи пользователям!\nЧто вы хотите сделать?", reply_markup=key.help)


def register_message_help(dp: Dispatcher):
    dp.register_message_handler(help, text="✅ Поддержка ✅")

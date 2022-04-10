from aiogram import Dispatcher, types
from Db import Database as data
from UsersDB import Users as User
import Keyboard as key
from client import bot
from sqlite_db import main_data as mdata


def Check_Call(call):
    cat = data.get_keyboard(0)
    for row in cat:
        if(row[0] == call):
            return True


async def command_start(message: types.Message):
    User.Check_id(message.from_user.id)
    await bot.send_message(message.from_user.id, f"*{message.from_user.first_name}*, приветствуем Вам в нашем боте", parse_mode='MarkdownV2')
    await bot.send_message(message.from_user.id, "Что будем делать?", reply_markup=key.Inline_key)


async def admin(message: types.Message):
    await bot.send_message(message.from_user.id, "Вы в меню администратора!\nЧто будем делать?", reply_markup=key.admin)


async def inline(message: types.Message):
    await bot.send_message(message.from_user.id, "Какие девушки Вам по душе?", reply_markup=key.categories)


async def category(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(text="Какие девушки Вам по душе?", reply_markup=key.categories)


async def inline_menu_back(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, "Категория: Девушки в возрасте " + age, reply_markup=Girl)


async def some_callback_handler(callback_query: types.CallbackQuery):
    if(Check_Call(callback_query.data) == True):
        global Girl
        global age
        age = callback_query.data
        Girl = key.get_girls_key(callback_query.data)
        await bot.answer_callback_query(callback_query.id)
        await callback_query.message.edit_text(text="Категория: Девушки в возрасте " + age, reply_markup=Girl)
    else:
        await callback_query.message.delete()
        await mdata.print_card(callback_query.data, callback_query.from_user.id)


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(admin, commands=['admin'])
    dp.register_message_handler(inline, text="Категории")
    dp.register_callback_query_handler(category, text='category')
    dp.register_callback_query_handler(inline_menu_back, text='Back')
    dp.register_callback_query_handler(
        some_callback_handler, lambda callback_query: True)

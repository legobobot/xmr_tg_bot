from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
import logging
import os
import json
from Db import Database as data
from UsersDB import Users as User
import Keyboard as key

API_TOKEN = "5223501086:AAGrVFoF2xkC0UvES0royfnjBLHlIm0VQ4o"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
ADMIN_ID = 349170112
global temp
temp = list()


class up(StatesGroup):
    SELECT_CATEG = State()  # Выбрать категорию
    UPLOAD_PHOTO = State()  # Добавить фотку
    ADD_DESC = State()  # Добавить описание
    UPLOAD_ARR = State()  # Добавить сам архив
    ADD_CAT = State()  # Добавить категорию
    DEL_CAT = State()  # Удалить категорию


# -----other_Function------


def Check_Call(call):
    cat = data.get_keyboard(0)
    for row in cat:
        if(row[0] == call):
            return True


def convert_to_binary(filename):
    with open(filename, "rb") as file:
        data_file = file.read()
    return data_file


# -------------------------


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    User.Check_id(message.from_user.id)
    await bot.send_message(message.from_user.id, f"*{message.from_user.first_name}*, приветствуем Вам в нашем боте", parse_mode='MarkdownV2')
    await bot.send_message(message.from_user.id, "Что будем делать?", reply_markup=key.Inline_key)


@dp.message_handler(commands=['37BSPO'])
async def admin(message: types.Message):
    await bot.send_message(message.from_user.id, "Вы в меню администратора!\nЧто будем делать?", reply_markup=key.admin)


@dp.message_handler(text="Категории")
async def inline(message: types.Message):
    await bot.send_message(message.from_user.id, "Какие девушки Вам по душе?", reply_markup=key.categories)


@dp.message_handler()
async def admin_menu(message: types.Message):
    if(message.from_user.id == ADMIN_ID):
        if(message.text == "Добавить файл"):
            await up.SELECT_CATEG.set()
            await bot.send_message(ADMIN_ID, "В какую категорию вы хотите добавить фото?", reply_markup=key.categories)

        if(message.text == "Удалить файл"):
            pass
        if(message.text == "Добавить категорию"):
            pass
        if(message.text == "Удалить категорию"):
            pass
        if(message.text == "Назад в главное меню"):
            pass


@dp.callback_query_handler(state=up.SELECT_CATEG)
async def select_category(callback_query: types.CallbackQuery, state: FSMContext):
    temp.append(callback_query.data)
    await state.finish()
    await up.UPLOAD_PHOTO.set()
    await bot.send_message(ADMIN_ID, "Загрузите вашу фотографию:")


@dp.message_handler(state=up.UPLOAD_PHOTO, content_types=['photo'])
async def add_photo(message: types.Message, state: FSMContext):
    print(temp)
    async with state.proxy() as dd:
        dd['photo'] = message.photo[0].file_id
    await state.finish()


@dp.callback_query_handler(text='category')
async def category(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(text="Какие девушки Вам по душе?", reply_markup=key.categories)


@dp.callback_query_handler(text='Back')
async def inline_menu_back(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, "Категория: Девушки в возрасте " + age, reply_markup=Girl)


@dp.callback_query_handler(lambda callback_query: True)
async def some_callback_handler(callback_query: types.CallbackQuery):
    if(Check_Call(callback_query.data) == True):
        global Girl
        global age
        age = callback_query.data
        Girl = key.get_girls_key(callback_query.data)
        await bot.answer_callback_query(callback_query.id)
        await callback_query.message.edit_text(text="Категория: Девушки в возрасте " + age, reply_markup=Girl)
    else:
        file = data.getGirls_preview(callback_query.data)
        buybtn = InlineKeyboardMarkup(row_width=3).row(
            InlineKeyboardButton(text="Назад", callback_data="Back"), InlineKeyboardButton(
                text="КУПИТЬ", callback_data="buy_arr"))
        await callback_query.message.delete()
        await bot.send_photo(callback_query.from_user.id, photo=file['File'], caption=file['Description'], parse_mode='MarkdownV2', reply_markup=buybtn)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

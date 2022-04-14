from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import Keyboard as key
from client import bot
from sqlite_db import AdminDATA


class FSMAdmin(StatesGroup):
    add_category = State()


async def select_category(message: types.Message):
    await FSMAdmin.add_category.set()
    await bot.send_message(message.from_user.id, "Напишите название новой категории товаров")


async def add_category(message: types.Message, state=FSMContext):
    AdminDATA.sqlite_add_category(message.text)
    await state.finish()
    categories = key.getNewKey()
    await bot.send_message(message.from_user.id, "ПОСЛЕ ПЕРЕЗАГРУЗКИ ваша клавиатура будет выглядеть так", reply_markup=categories)


def register_handlers_add_cat(dp: Dispatcher):
    dp.register_message_handler(
        select_category, text="Добавить категорию", state=None)
    dp.register_message_handler(add_category, state=FSMAdmin.add_category)

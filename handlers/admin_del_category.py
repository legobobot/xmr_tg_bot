from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import Keyboard as key
from client import bot
from sqlite_db import AdminDATA


class FSMAdmin(StatesGroup):
    del_category = State()


async def select_category(message: types.Message):
    await FSMAdmin.del_category.set()
    await bot.send_message(message.from_user.id, "Выберите категорию, которую хотите удалить", reply_markup=key.categories)


async def del_cat(callback_query: types.CallbackQuery, state: FSMContext):
    AdminDATA.sqlite_del_category(callback_query.data)
    await state.finish()
    categories = key.getNewKey()
    await bot.send_message(callback_query.from_user.id, "Категория была успешно удалена!\nПОСЛЕ ПЕРЕЗАПУСКА БОТА ваша клавиатура будет выглядеть так", reply_markup=categories)


def register_handlers_del_cat(dp: Dispatcher):
    dp.register_message_handler(
        select_category, text="Удалить категорию", state=None)
    dp.register_callback_query_handler(del_cat, state=FSMAdmin.del_category)

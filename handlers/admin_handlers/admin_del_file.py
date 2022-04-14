from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import Keyboard as key
from client import bot
from sqlite_db import AdminDATA as adata


class FSMAdmin(StatesGroup):
    one = State()
    file = State()

# ---------add_file-----------------------


async def select_category(message: types.Message):
    await FSMAdmin.one.set()
    await bot.send_message(message.from_user.id, "Выберите категорию, в которой хотите удалить лот", reply_markup=key.categories)


async def select_file(callback_query: types.CallbackQuery, state=FSMContext):
    Girl = key.get_girls_key(callback_query.data)
    await FSMAdmin.next()
    await callback_query.message.edit_text("Что вы хотите удалить?", reply_markup=Girl)


async def del_file(callback_query: types.CallbackQuery, state: FSMContext):
    adata.sqlite_del_file(callback_query.data)
    await state.finish()
    await callback_query.message.edit_text("Лот был успешно удален!")


async def cancel(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, "Была произведена отмена операции!")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        select_category, text="Удалить файл", state=None)
    dp.register_callback_query_handler(select_file, state=FSMAdmin.one)
    dp.register_callback_query_handler(del_file, state=FSMAdmin.file)
    dp.register_message_handler(cancel, state="*", commands='отмена')
    dp.register_message_handler(cancel, Text(
        equals='отмена', ignore_case=True), state="*")

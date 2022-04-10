from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import Keyboard as key
from client import bot
from sqlite_db import AdminDATA


class FSMAdmin(StatesGroup):
    category = State()
    import_file = State()
    card_name = State()
    description = State()
    Import_photo = State()

# ---------add_file-----------------------


async def select_category(message: types.Message):
    await FSMAdmin.category.set()
    await bot.send_message(message.from_user.id, "Выберите категорию, в которую хотите добавить новый пункт: ", reply_markup=key.categories)


async def load_category(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as DT:
        DT['category'] = callback_query.data
    await FSMAdmin.next()
    await bot.send_message(callback_query.from_user.id, "Загрузите ваш архив")


async def load_file(message: types.Message, state=FSMContext):
    async with state.proxy() as DT:
        DT['file'] = message.document.file_id
    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, "Окей, файл был успешно загружен, теперь мы переходим к добавлению карточки товара")
    await bot.send_message(message.from_user.id, "Теперь дайте название карточки товара:")


async def card_name(message: types.Message, state=FSMContext):
    async with state.proxy() as DT:
        DT['card_name'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, "Теперь отправьте мне описание вашей карточки")


async def description(message: types.Message, state=FSMContext):
    async with state.proxy() as DT:
        DT['description'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, "Все прошло успешно\nТеперь, завершающим этапом я жду от Вас фото товара")


async def load_photo(message: types.Message, state=FSMContext):
    async with state.proxy() as DT:
        DT['photo'] = message.photo[0].file_id
    await bot.send_message(message.from_user.id, "Карточка была успешна создана!\n")
    await AdminDATA.sqlite_add_commads(state)
    await state.finish()


async def cancel(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, "Была произведена отмена операции!")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        select_category, text="Добавить файл", state=None)
    dp.register_callback_query_handler(load_category, state=FSMAdmin.category)
    dp.register_message_handler(load_file, content_types=[
                                'document'], state=FSMAdmin.import_file)
    dp.register_message_handler(card_name, state=FSMAdmin.card_name)
    dp.register_message_handler(description, state=FSMAdmin.description)
    dp.register_message_handler(load_photo, content_types=[
                                'photo'], state=FSMAdmin.Import_photo)
    dp.register_message_handler(cancel, state="*", commands='отмена')
    dp.register_message_handler(cancel, Text(
        equals='отмена', ignore_case=True), state="*")

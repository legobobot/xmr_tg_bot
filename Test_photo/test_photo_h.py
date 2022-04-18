from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite_db.UserDB as user
from Test_photo import key as test_key
from Test_photo import sql_commands as sq
from client import bot
import Keyboard as key


class FSMtest(StatesGroup):
    updel = State()
    agreement = State()
    add_file = State()

# standart_keys-----------------------------------------


async def start_test(message: types.Message):
    await bot.send_message(message.from_user.id, "Вы перешли в меню халявы", reply_markup=test_key.morebtn)


async def back_to_menu(message: types.Message):
    await message.answer("Вы в главном меню!", reply_markup=key.Inline_key)


async def more(message: types.Message):
    if(sq.get_user_try_number(message.from_user.id) <= sq.max_s_photo()):
        photo = sq.get_one(message.from_user.id)
        await bot.send_photo(message.from_user.id, photo=photo, caption=f'_Осталось бесплатный фото:_ *{(sq.max_s_photo() - sq.get_user_try_number(message.from_user.id))+2}*', parse_mode='MarkdownV2')
    else:
        await bot.send_message(message.from_user.id,
                               "*Ваши бесплатные фото закончились*\n\nВы можете ✅*купить один из паков*✅, чтобы порадовать себя, либо же ждать следующего обновления категории \n♻️_*Бесплатное*_♻️",
                               parse_mode='MarkdownV2')


async def test_photo_edit(message: types.Message):
    await bot.send_message(message.from_user.id, "Вы перешли в меню редактирования тестовых показов", reply_markup=test_key.admin_menu)


async def back_to_admin(message: types.Message):
    await bot.send_message(message.from_user.id, "Вы в меню Администратора!", reply_markup=key.admin)

# DEL_and_ADD_file------------------------------------


async def del_file(message: types.Message):
    keys = sq.get_all_file()
    global temp_keys_in_test_photo
    temp_keys_in_test_photo = InlineKeyboardMarkup(row_width=1)
    for i in keys:
        temp_keys_in_test_photo.insert(
            InlineKeyboardButton(text=i[0], callback_data=i[0]))
    await FSMtest.updel.set()
    await bot.send_message(message.from_user.id, "Выберите удаляемый объект", reply_markup=temp_keys_in_test_photo)


async def proof(callback_query: types.CallbackQuery, state=FSMContext):
    photo = sq.send_file_prev(callback_query.data)
    async with state.proxy() as dt:
        dt['photo_id'] = photo
    agree = InlineKeyboardMarkup(row_width=1).row(InlineKeyboardButton(
        text="Да", callback_data="yes"), InlineKeyboardButton(text="Нет", callback_data="no"))
    await FSMtest.next()
    await bot.send_photo(callback_query.from_user.id, photo=photo[0], caption="Удалить эту фотографию?", reply_markup=agree)


async def yes_on_proof(callback_query: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as dt:
        sq.del_file(dt['photo_id'][0])
    await state.finish()
    await bot.send_message(callback_query.from_user.id, "Фото было удалено!")


async def no_on_proof(callback_query: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await FSMtest.updel.set()
    await callback_query.message.edit_text("Выберите удаляемый объект", reply=temp_keys_in_test_photo)
# -----------------------------------------------------------


async def add_file(message: types.Message):
    await FSMtest.add_file.set()
    await bot.send_message(message.from_user.id, "Пришлите сюда вашу фотографию")


async def upload_file(message: types.Message, state=FSMContext):
    sq.add_file(message.photo[0].file_id)
    await state.finish()
    await bot.send_message(message.from_user.id, "Фото было успещно загружено!")


def register_test_photo(dp: Dispatcher):
    dp.register_message_handler(
        start_test, text="🔥🔥🔥 Халявные Нюдсы 🔥🔥🔥")
    dp.register_message_handler(back_to_menu, text="↩️ Главное меню")
    dp.register_message_handler(more, text="🔞Nudes🔞")
    dp.register_message_handler(
        test_photo_edit, text="Редактировать превью фотографии")
    dp.register_message_handler(back_to_admin, text="Назад")
    # Удалить файл-------------------------------------------------------
    dp.register_message_handler(del_file, text="Удалить", state=None)
    dp.register_callback_query_handler(proof, state=FSMtest.updel)
    dp.register_callback_query_handler(
        yes_on_proof, text='yes', state=FSMtest.agreement)
    dp.register_callback_query_handler(
        no_on_proof, text='no', state=FSMtest.agreement)
    # Добавить файл-------------------------------------------------------
    dp.register_message_handler(add_file, text="Добавить", state=None)
    dp.register_message_handler(upload_file, content_types=[
                                'photo'], state=FSMtest.add_file)

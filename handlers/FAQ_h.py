from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from client import bot


user_agreement = InlineKeyboardButton(
    text="Пользовательское соглашение",
    url="https://telegra.ph/Publichnaya-oferta-na-zaklyuchenie-licenzionnogo-dogovora-04-23",
)
our_projects = InlineKeyboardButton(text="Наши проекты", callback_data="our_projects")
referal_system = InlineKeyboardButton(
    text="Реферальная система",
    url="https://telegra.ph/Kak-zarabotat-na-referalnoj-sisteme-04-23",
)
keyboard = InlineKeyboardMarkup(row_width=1).add(
    our_projects, referal_system, user_agreement
)
# button_projects-------------------------
free_group = InlineKeyboardButton(text="Отборный СОК", url="https://t.me/otborniy_SOK")
VIP_group = InlineKeyboardButton(
    text="VIP Группа", url="https://t.me/Otbotniy_SOK_VIP_bot"
)
reviews = InlineKeyboardButton(text="Отзывы", url="https://t.me/otzivi_os_store")
updateG = InlineKeyboardButton(
    text="Обновления бота", url="https://t.me/os_store_update"
)
back = InlineKeyboardButton(text="Назад", callback_data="FAQ_menu")
project = InlineKeyboardMarkup(row_width=1).add(
    free_group, VIP_group, reviews, updateG, back
)


# button_projects-------------------------
async def FAQ(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        "<i><b>Выберете нужный Вам пункт</b></i>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


async def our_projects(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    await call.message.edit_text(
        text="<i><b>Наши проекты:</b></i>", parse_mode="HTML", reply_markup=project
    )


async def back(call: types.CallbackQuery):
    await call.message.edit_text(
        text="<i><b>Выберете нужный Вам пункт</b></i>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


def register_FAQ_information(dp: Dispatcher):
    dp.register_message_handler(FAQ, text="ℹ️ FAQ")
    dp.register_callback_query_handler(back, text="FAQ_menu")
    dp.register_callback_query_handler(our_projects, text="our_projects")

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import Keyboard as key
from client import bot
from sqlite_db import main_data as main_data



class FSMhelp(StatesGroup):
    answer = State()
    review = State()


async def help(message: types.Message):
    await message.answer(
        "Вы перешли в меню помощи пользователям!\nЧто вы хотите сделать?",
        reply_markup=key.help,
    )


async def link_with_support(message: types.Message):
    await FSMhelp.answer.set()
    await bot.send_message(
        message.from_user.id, "Пожалуйста, опишите мне Вашу проблему!"
    )


async def get_link_text(message: types.Message, state=FSMContext):
    await bot.send_message(
        chat_id=-1001754288050,
        text=f'<b>Обращение</b> от пользователя <b><i>{message.from_user.id}</i></b> \n\n"<i>{message.text}</i>"',
        parse_mode="HTML",
    )
    await state.finish()
    await bot.send_message(
        message.from_user.id,
        "Ваша заявка была принята в рассмотрении! \nНаш специалист в скорем времени свяжется с Вами для уточнее проблемы и о способе ее решения!",
        reply_markup=key.help,
    )


async def Write_a_review(message: types.Message):
    await FSMhelp.review.set()
    await bot.send_message(
        message.from_user.id, "Пожалуйста, отправте свой отзыв мне в виде сообщения!"
    )


async def get_review(message: types.Message, state=FSMContext):
    await bot.send_message(
        chat_id=-1001760732003,
        text=f"<b>Отзыв от пользователя</b> <i>{message.from_user.id}</i>\n"
        + f'\n"<i>{message.text}</i>"',
        parse_mode="HTML",
    )
    await bot.send_message(
        message.from_user.id, "Большое Вам спасибо за отзыв!", reply_markup=key.help
    )
    await state.finish()


def register_message_help(dp: Dispatcher):
    dp.register_message_handler(help, text="✅ Поддержка ✅")
    dp.register_message_handler(link_with_support, text="📞 Связь с поддержкой")
    dp.register_message_handler(get_link_text, state=FSMhelp.answer)
    dp.register_message_handler(Write_a_review, text="📝 Оставить отзыв")
    dp.register_message_handler(get_review, state=FSMhelp.review)

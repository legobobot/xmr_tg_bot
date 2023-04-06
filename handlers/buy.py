from aiogram import Dispatcher, types
from sqlite_db import UserDB as user
import Keyboard as key
from client import bot
from sqlite_db import moneyDB as money


def get_name(title):
    temp = ""
    for i in range(len(title)):
        if title[i] == "(":
            break
        temp += title[i]
    return temp


async def process_buy_command(call: types.CallbackQuery):
    girl = int(user.get_last_girl(call.from_user.id)[-4:-1])
    if(int(money.get_balans(call.from_user.id)) >= girl):
        money.add_purchased(call.from_user.id)
        money.minus_money(call.from_user.id, girl)
        await bot.send_message(call.from_user.id, "<b>Ваша покупка была успешно совершена!</b>", parse_mode='HTML')
        await bot.send_message(call.from_user.id, "<i>Загрузка файла....</i>", parse_mode='HTML')
        await bot.send_document(call.from_user.id, document=money.get_file(call.from_user.id), caption="<b>Ваш архив был успешно загружен!</b>\n на здоровье😘", parse_mode='HTML')
    else:
        await bot.send_message(call.from_user.id, "На вашем счете недостаточно средств!", reply_markup=key.little_money)


def register_pay_handler(dp: Dispatcher):
    dp.register_callback_query_handler(process_buy_command, text='buy_arr')

from aiogram import Dispatcher, types
import Keyboard as key
from client import bot, ADMIN_ID
from sqlite_db import AdminDATA as admin


async def statistic(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await bot.send_message(message.from_user.id, "Вы в меню статистики бота!", reply_markup=key.statbtn)


async def state(message: types.Message):
    await bot.send_message(message.from_user.id, f"<b>Всего новых заказов:</b> {admin.get_all_orders()}\n" +
                           f"<b>На сумму:</b> {admin.get_today_pay()} рублей", parse_mode='HTML')


async def dell(message: types.Message):
    admin.del_today_stat()
    await bot.send_message(message.from_user.id, "Статистика на сегодня была полностю очищена!")


def register_admin_command_handler(dp: Dispatcher):
    dp.register_message_handler(statistic, text="Статистика")
    dp.register_message_handler(state, text="Статистика за сегодня")
    dp.register_message_handler(dell, text="Очистить")

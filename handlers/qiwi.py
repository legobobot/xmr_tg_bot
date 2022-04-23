from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from client import bot, QIWI_TOKEN
from sqlite_db import moneyDB as money
from glQiwiApi import QiwiP2PClient

qiwi_p2p_client = QiwiP2PClient(secret_p2p=QIWI_TOKEN)


def is_number(_str):
    try:
        int(_str)
        return True
    except ValueError:
        return False


class FSMqiwi(StatesGroup):
    set_money = State()
    payment = State()


async def set_money(message: types.Message, state=FSMContext):
    await bot.send_message(
        message.from_user.id,
        "<b>МИНИМАЛЬНАЯ СУММА ПОПОЛНЕНИЯ - <code>10</code> РУБЛЕЙ</b>\n\nВведите сумму пополнения: ",
        parse_mode="HTML",
    )
    await FSMqiwi.set_money.set()


async def handle_creation_of_payment(message: types.Message, state: FSMContext):
    if is_number(message.text) == True and int(message.text) >= 10:
        async with qiwi_p2p_client:
            bill = await qiwi_p2p_client.create_p2p_bill(amount=message.text)
            money.add_payments_par(
                user_id=message.from_user.id, money=message.text, bill_id=bill.id
            )
        async with state.proxy() as tt:
            tt["set_money"] = message.text
            tt["bill_id"] = bill.id
        await bot.send_message(
            message.from_user.id,
            text=f"Ссылка для пополнения баланса:\n {bill.pay_url}\n\nВы можете пополнить баланс в течение <b>45 минут</b>!!!",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(row_width=1).row(
                InlineKeyboardButton(text="Отменить", callback_data="CANCEL_PAY"),
                InlineKeyboardButton(text="ОПЛАТИТЬ", url=bill.pay_url),
                InlineKeyboardButton(text="Проверить", callback_data="CHECK_PAY"),
            ),
        )
        await FSMqiwi.next()
        await state.update_data(bill=bill)
    else:
        await state.finish()
        await FSMqiwi.set_money.set()
        await bot.send_message(
            message.from_user.id,
            "<b>Вы ввели сумму меньше 10 рублей, либо допустили ошибку!</b>\nПожалуйста, введите сумму пополнения еще раз: ",
            parse_mode="HTML",
        )


async def handle_successful_payment(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        bill: bill = data.get("bill")
        pay_money: pay_money = data.get("set_money")
    if await qiwi_p2p_client.check_if_bill_was_paid(bill):
        await bot.send_message(
            call.from_user.id,
            f"Вы успешно пополнили свой счет на <code>{pay_money}</code> рублей",
            parse_mode="HTML",
        )
        money.add_money(call.from_user.id, money.get_added_money(call.from_user.id))
        await state.finish()
    else:
        await call.answer("Не оплачено!")


async def cancel(call: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        bill: bill = data.get("bill")
        id: id = data.get("bill_id")
    await state.finish()
    await qiwi_p2p_client.reject_bill(bill)
    await call.message.delete()
    money.delete_bill_id(id)
    await bot.send_message(call.from_user.id, "Платеж был успешно отклонен!")


def register_buy_handler(dp: Dispatcher):
    dp.register_callback_query_handler(set_money, text="add_money", state=None)
    dp.register_message_handler(handle_creation_of_payment, state=FSMqiwi.set_money)
    dp.register_callback_query_handler(cancel, text="CANCEL_PAY", state=FSMqiwi.payment)
    dp.register_callback_query_handler(
        handle_successful_payment, text="CHECK_PAY", state=FSMqiwi.payment
    )

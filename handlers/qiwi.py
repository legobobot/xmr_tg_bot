from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
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


async def set_money(message: types.Message, state=FSMContext):
    await bot.send_message(message.from_user.id, "Введите сумму пополнения: ")
    await state.set_state("set_money")


async def handle_creation_of_payment(message: types.Message, state: FSMContext):
    if(is_number(message.text) == True):
        async with qiwi_p2p_client:
            bill = await qiwi_p2p_client.create_p2p_bill(amount=message.text)
            money.add_payments_par(
                user_id=message.from_user.id, money=message.text, bill_id=bill.id)
        await bot.send_message(message.from_user.id, text=f"Ссылка для пополнения баланса:\n {bill.pay_url}\n\nВы можете пополнить баланс в течение <b>45 минут</b>!!!",
                               parse_mode='HTML',
                               reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Отменить пополнение", callback_data="CANCEL_PAY")))
        await state.set_state("payment")
        await state.update_data(bill=bill)
    else:
        await state.finish()
        await state.set_state("set_money")
        await bot.send_message(message.from_user.id,
                               "<b>Неправильный ввод!</b>\nПожалуйста, введите сумму пополнения <b>ЧИСЛОМ</b>: ", parse_mode='HTML')


async def handle_successful_payment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        bill: bill = data.get("bill")
    if await qiwi_p2p_client.check_if_bill_was_paid(bill):
        await message.answer(f"Вы успешно пополнили свой счет на <code>{money.get_added_money(message.from_user.id)}</code> рублей", parse_mode='HTML')
        money.add_money(message.from_user.id,
                        money.get_added_money(message.from_user.id))
        await state.finish()
    else:
        await message.answer("Invoice was not paid")


async def cancel(call: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        bill: bill = data.get("bill")

    await bot.send_message(call.from_user.id, f"Вы успешно пополнили свой счет на <code>{money.get_added_money(call.from_user.id)}</code> рублей", parse_mode='HTML')
    money.add_money(call.from_user.id,
                    money.get_added_money(call.from_user.id))
    await state.finish()
    await qiwi_p2p_client.reject_bill(bill)
    await call.message.delete()
    money.delete_bill_id(call.from_user.id)
    await bot.send_message(call.from_user.id, "Платеж был успешно отклонен!")


def register_buy_handler(dp: Dispatcher):
    dp.register_callback_query_handler(
        set_money, text="add_money", state=None)
    dp.register_message_handler(handle_creation_of_payment, state="set_money")
    dp.register_callback_query_handler(
        cancel, text="CANCEL_PAY", state="payment")
    dp.register_message_handler(handle_successful_payment, state="payment")

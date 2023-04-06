from monero.wallet import Wallet
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from client import bot, QIWI_TOKEN
from sqlite_db import moneyDB as money
import random

# Подключение к локальной ноде
w = Wallet(port=18082)

class FSMmonero(StatesGroup):
    set_money = State()
    payment = State()

async def set_money(message: types.Message, state=FSMContext):
    await bot.send_message(
        message.from_user.id,
        "<b>МИНИМАЛЬНАЯ СУММА ПОПОЛНЕНИЯ - <code>10</code> РУБЛЕЙ</b>\n\nВведите сумму пополнения: ",
        parse_mode="HTML",
    )
    await FSMmonero.set_money.set()

async def handle_creation_of_payment(message: types.Message, state: FSMContext):
    if is_number(message.text) == True and int(message.text) >= 0:
        destination_address = '46PrVgGThpJf1nxshyusgKUsRLF9oYwntgdN6vFfo1KgZpNRYZ1TpV8p36yvJBmZ7YX3qEMELm2GvTAJGjF43NicJZKvbW8'
        payment_id = str(random.randint(100000, 999999))
        amount = int(message.text) * 1000000000000  # Amount in piconero (1 XMR = 1000000000000 piconero)
        tx = await w.transfer(destination_address, amount, payment_id=payment_id)

        # Save the transaction id to the database
        money.add_payments_par(
            user_id=message.from_user.id, money=message.text, bill_id=tx.tx_hash()
        )

        await state.update_data(payment_id=payment_id, amount=message.text)
        await bot.send_message(
            message.from_user.id,
            text=f"<b>Ожидаем зачисления...</b>\n\n"
            f"Отправьте номер транзакции, чтобы проверить изменение баланса или нажмите /cancel, чтобы отменить операцию.",
            parse_mode="HTML",
        )
        await FSMmonero.payment.set()

async def check_balance(message: types.Message):
    payments = money.get_payments_by_user(message.from_user.id)
    if payments:
        payment = payments[-1]
        tx_hash = payment[3]
        tx_info = await w.get_transfer_by_txid(tx_hash)
        if tx_info.confirmations > 0:
            balance = await w.get_balance()
            await bot.send_message(
                message.from_user.id,
                text=f"<b>Баланс:</b> {balance[0] / 1000000000000} XMR\n\n<b>Номер транзакции:</b> {tx_hash}",
                parse_mode="HTML",
            )
        else:
            await bot.send_message(
                message.from_user.id,
                text="<b>Транзакция не подтверждена.</b>",
                parse_mode="HTML",
            )
    else:
        await bot

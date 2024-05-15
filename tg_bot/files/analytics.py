import hashlib

import pandas as pd
import sqlite3
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from tg_bot.data.config import TRANSACTION_PATH, INCOME_PATH, EXPENSES_PATH, BALANCES_PATH
from tg_bot.data.loader import bot, db
from tg_bot.keyboards.reply import menu_statistics, main_kb, back_btn
from tg_bot.states.analytic_state import AnalyticsState


async def transactions(telegram_id):
    conn = sqlite3.connect('acc.db')
    df = pd.read_sql_query(f"SELECT * FROM transactions WHERE user_id = {telegram_id}", conn)
    df.to_excel(TRANSACTION_PATH)


async def income(telegram_id):
    conn = sqlite3.connect('acc.db')
    df = pd.read_sql_query(f"SELECT * FROM transactions WHERE user_id = {telegram_id} AND type_title = 'income'", conn)
    df.to_excel(INCOME_PATH)


async def expenses(telegram_id):
    conn = sqlite3.connect('acc.db')
    df = pd.read_sql_query(f"SELECT * FROM transactions WHERE user_id = {telegram_id} AND type_title = 'expenses'",
                           conn)
    df.to_excel(EXPENSES_PATH)


async def balance(telegram_id):
    conn = sqlite3.connect('acc.db')
    df = pd.read_sql_query(f"SELECT * FROM users WHERE telegram_id = {telegram_id}", conn)
    df.to_excel(BALANCES_PATH)


analytics_router = Router()


@analytics_router.message(F.text == '📈Аналитика')
async def main_analiz_menu(message: types.Message, state: FSMContext):
    await message.answer('Введите пароль', reply_markup=back_btn())
    await state.set_state(AnalyticsState.password)


@analytics_router.message(AnalyticsState.password)
async def check_password_analytics(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == '🔙 Назад':
        await message.answer('Действие отменено', reply_markup=main_kb())
        await state.clear()
    else:
        if db.select_password(chat_id)[0] == hashlib.sha256(message.text.encode('utf-8')).hexdigest():
            await message.answer('Выберите действие', reply_markup=menu_statistics())
            await state.set_state(AnalyticsState.step1)
        else:
            await message.answer('Не верный пароль, введите правильный пароль', reply_markup=back_btn())
            await state.set_state(AnalyticsState.password)


@analytics_router.message(AnalyticsState.step1)
async def main_menu_state(message: types.Message, state: FSMContext):
    if message.text == '🔙 Назад':
        await message.answer('Главное меню', reply_markup=main_kb())
        await state.clear()
    elif message.text == 'Доходы':
        count_incomes = db.select_count_of_incomes()[0][0]
        usd_incomes = db.select_usd_income(telegram_id=message.chat.id)[0][0]
        uzs_income = db.select_uzs_income(telegram_id=message.chat.id)[0][0]
        await message.answer(f'<b>Доходы:</b>\n\n'
                             f'<b>Кол-во транзакций:</b> {count_incomes}\n'
                             f'<b>Доходы в USD💲:</b> {usd_incomes}\n'
                             f'<b>Доходы в UZS:</b> {uzs_income}')
        await income(message.chat.id)
        document = FSInputFile(path=INCOME_PATH)
        await bot.send_document(message.chat.id, document=document)
        await state.set_state(AnalyticsState.step1)
    elif message.text == 'Расходы':
        count_expenses = db.select_count_of_expenses()[0][0]
        usd_expenses = db.select_usd_expenses(telegram_id=message.chat.id)[0][0]
        uzs_expenses = db.select_uzs_expenses(telegram_id=message.chat.id)[0][0]
        await message.answer(f'<b>Расходы:</b>\n\n'
                             f'<b>Кол-во транзакций:</b> {count_expenses}\n'
                             f'<b>Расходы в USD💲:</b> {usd_expenses}\n'
                             f'<b>Расходы в UZS:</b> {uzs_expenses}')
        await expenses(message.chat.id)
        document = FSInputFile(path=EXPENSES_PATH)
        await bot.send_document(message.chat.id, document=document)
        await state.set_state(AnalyticsState.step1)
    elif message.text == 'Баланс':
        await balance(message.chat.id)
        db_balance = db.get_user_by_id(message.chat.id)
        uzs_balance = (db_balance[3] + db_balance[6] +
                       db_balance[10] + db_balance[11]
                       + db_balance[12])
        usd_balance = (db_balance[4] + db_balance[5] + db_balance[7] + db_balance[8] + db_balance[9])
        await message.answer(f'<b>Общий баланс (UZS):</b>➡️  {uzs_balance}\n\n'
                             f'<b>Общий баланс (USD):</b>➡️  {usd_balance}\n\n'
                             f'<b>Наличные сумы:</b>➡️  {db_balance[3]}\n'
                             f'<b>Наличные доллары:</b>➡️  {db_balance[4]}\n'
                             f'<b>Карта валютный (USD) 1:</b>➡️  {db_balance[5]}\n'
                             f'<b>Карта суммовой (UZS) 1:</b>➡️  {db_balance[6]}\n'
                             f'<b>Карта валютный (USD) 2:</b>➡️  {db_balance[7]}\n'
                             f'<b>Карта валютный (USD) 3:</b>➡️  {db_balance[8]}\n'
                             f'<b>Карта валютный (USD) 4:</b>➡️  {db_balance[9]}\n'
                             f'<b>Карта суммовой (UZS) 2:</b>➡️  {db_balance[10]}\n'
                             f'<b>Карта суммовой (UZS) 3:</b>➡️  {db_balance[11]}\n'
                             f'<b>Карта суммовой (UZS) 4:</b>➡️  {db_balance[12]}\n')
        document = FSInputFile(path=BALANCES_PATH)
        await bot.send_document(message.chat.id, document=document)
        await state.set_state(AnalyticsState.step1)

    elif message.text == 'Транзакции':
        await transactions(message.chat.id)
        document = FSInputFile(path=TRANSACTION_PATH)
        await bot.send_document(message.chat.id, document=document)
        await state.set_state(AnalyticsState.step1)
    else:
        await message.answer('Выберите действие', reply_markup=menu_statistics())
        await state.set_state(AnalyticsState.step1)


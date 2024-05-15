import hashlib

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from tg_bot.data.loader import db
from tg_bot.keyboards.reply import income_types, accept_transactions, main_kb, back_btn, uzs_usd_kb, conversion_usd_btn, \
    conversion_uzs_btn
from tg_bot.states.incomes_state import NewIncome

add_income_router = Router()


@add_income_router.message(F.text == '➕ Доходы')
async def add_incomes(message: types.Message, state: FSMContext):
    await message.answer('Введите пароль', reply_markup=ReplyKeyboardRemove())
    await state.set_state(NewIncome.password)


@add_income_router.message(NewIncome.password)
async def check_password_incomes(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == '🔙 Назад':
        await message.answer('Действие отменено', reply_markup=main_kb())
        await state.clear()
    else:
        if db.select_password(chat_id)[0] == hashlib.sha256(message.text.encode('utf-8')).hexdigest():
            await message.answer('Выберите валюту', reply_markup=uzs_usd_kb())
            await state.set_state(NewIncome.uzs_usd)
        else:
            await message.answer('Не верный пароль, введите правильный пароль', reply_markup=back_btn())
            await state.set_state(NewIncome.password)


@add_income_router.message(NewIncome.uzs_usd)
async def uzs_usd_state(message: types.Message, state: FSMContext):
    if message.text == '🔙 Назад':
        await message.answer('Действие отменено', reply_markup=main_kb())
        await state.clear()
    else:
        if message.text == 'UZS':
            await state.update_data(uzs_usd='UZS')
            await message.answer('Выберите категорию', reply_markup=conversion_uzs_btn())
            await state.set_state(NewIncome.category)
        elif message.text == 'USD':
            await state.update_data(uzs_usd='USD')
            await message.answer('Выберите категорию', reply_markup=conversion_usd_btn())
            await state.set_state(NewIncome.category)
        else:
            await message.answer('Выберит одно из двух', reply_markup=uzs_usd_kb())
            await state.set_state(NewIncome.uzs_usd)


def categories():
    category = [i[0] for i in db.select_incomes()]
    return category


@add_income_router.message(NewIncome.category)
async def state_category_income(message: types.Message, state: FSMContext):
    category = message.text
    if category in [i[0] for i in db.select_incomes()] or message.text == '🔙 Назад':
        st = await state.get_data()
        if st['uzs_usd'] == 'USD':
            if category in [i[0] for i in db.select_incomes_by_currency('usd')]:
                await message.answer('Введите сумму в долларах:\n',
                                     reply_markup=back_btn())
                await state.update_data(category=category)
                await state.set_state(NewIncome.quantity)
            elif category == '🔙 Назад':
                await message.answer('Выберите валюту', reply_markup=uzs_usd_kb())
                await state.set_state(NewIncome.uzs_usd)

            else:
                await message.answer('Такой категории нет')
                await state.set_state(NewIncome.category)
        elif st['uzs_usd'] == 'UZS':
            if category in [i[0] for i in db.select_incomes_by_currency('uzs')]:
                await message.answer('Введите сумму в сумах:\n',
                                     reply_markup=back_btn())
                await state.update_data(category=category)
                await state.set_state(NewIncome.quantity)
            elif category == '🔙 Назад':
                await message.answer('Выберите валюту', reply_markup=uzs_usd_kb())
                await state.set_state(NewIncome.uzs_usd)

            else:
                await message.answer('Такой категории нет')
                await state.set_state(NewIncome.category)
    else:
        await message.answer('Такой категории нет')
        await state.set_state(NewIncome.category)


@add_income_router.message(NewIncome.quantity)
async def state_quantity_income(message: types.Message, state: FSMContext):
    st = await state.get_data()
    if message.text == '🔙 Назад':
        if st['uzs_usd'] == 'UZS':
            await state.update_data(uzs_usd='UZS')
            await message.answer('Выберите категорию', reply_markup=conversion_uzs_btn())
            await state.set_state(NewIncome.category)
        elif st['uzs_usd'] == 'USD':
            await state.update_data(uzs_usd='USD')
            await message.answer('Выберите категорию', reply_markup=conversion_usd_btn())
            await state.set_state(NewIncome.category)
    else:
        try:
            quantity = int(message.text)
            if isinstance(quantity, int):
                await message.answer('Введите описание')
                await state.update_data(quantity=message.text)
                await state.set_state(NewIncome.description)
        except ValueError:
            await message.answer('Введите сумму корректно -> 20000')
            await state.set_state(NewIncome.quantity)


@add_income_router.message(NewIncome.description)
async def state_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    st = await state.get_data()
    await message.answer(f'<b>Доход:</b>\n\n'
                         f'<b>Сумма:</b> {st["quantity"]}\n'
                         f'<b>Валюта:</b> {st["uzs_usd"]}\n'
                         f'<b>Описание:</b> {st["description"]}\n'
                         f'<b>Категория:</b> {st["category"]}\n', reply_markup=accept_transactions())
    await state.set_state(NewIncome.accept)


@add_income_router.message(NewIncome.accept)
async def state_accept(message: types.Message, state: FSMContext):
    if message.text == 'Подтвердить':
        st = await state.get_data()
        db.insert_transaction_income(user_id=message.chat.id,
                                     type_title='income',
                                     quantity=st['quantity'],
                                     description=st['description'],
                                     income_type=st['category'],
                                     uzs_usd=st['uzs_usd'])
        await state.clear()
        await message.answer('Действие подтверждено', reply_markup=main_kb())
        category = st['category']
        db_quantity = db.select_quantity(category=f'"{category}"', telegram_id=message.chat.id)[0]
        insert_quantity = int(db_quantity) + int(st['quantity'])
        db.change_quantity(category=f'"{category}"', telegram_id=message.chat.id, quantity=insert_quantity)

    elif message.text == 'Отменить':
        await state.clear()
        await message.answer('Действие отменено', reply_markup=main_kb())
    else:
        await message.answer('Выберите действие', reply_markup=accept_transactions())
        await state.set_state(NewIncome.accept)

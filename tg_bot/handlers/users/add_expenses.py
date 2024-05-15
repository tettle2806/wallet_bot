import hashlib

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from tg_bot.data.loader import db
from tg_bot.keyboards.reply import expense_types, subcategory_types, main_kb, back_btn, income_types, \
    accept_transactions, uzs_usd_kb
from tg_bot.states.expenses_state import NewExpenses

expenses_router = Router()


@expenses_router.message(F.text == '➖ Расходы')
async def add_expenses(message: types.Message, state: FSMContext):
    await message.answer('Введите пароль', reply_markup=ReplyKeyboardRemove())
    await state.set_state(NewExpenses.password)


@expenses_router.message(NewExpenses.password)
async def check_password_expenses(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == '🔙 Назад':
        await message.answer('Действие отменено', reply_markup=main_kb())
        await state.clear()
    else:
        if db.select_password(chat_id)[0] == hashlib.sha256(message.text.encode('utf-8')).hexdigest():
            await message.answer('Выберите валюту', reply_markup=uzs_usd_kb())
            await state.set_state(NewExpenses.uzs_usd)
        else:
            await message.answer('Не верный пароль, введите правильный пароль', reply_markup=back_btn())
            await state.set_state(NewExpenses.password)


@expenses_router.message(NewExpenses.uzs_usd)
async def state_uzs_usd(message: types.Message, state: FSMContext):
    if message.text == '🔙 Назад':
        await message.answer('Действие отменено', reply_markup=main_kb())
        await state.clear()
    else:
        if message.text == 'UZS':
            await state.update_data(uzs_usd='UZS')
            await message.answer('Выберите категорию', reply_markup=expense_types())
            await state.set_state(NewExpenses.category)
        elif message.text == 'USD':
            await state.update_data(uzs_usd='USD')
            await message.answer('Выберите категорию', reply_markup=expense_types())
            await state.set_state(NewExpenses.category)
        else:
            await message.answer('Выберит одно из двух', reply_markup=uzs_usd_kb())
            await state.set_state(NewExpenses.uzs_usd)


def sub_categories(category: str):
    category = [i[0] for i in db.select_subcategory(category_title=category)]
    return category


@expenses_router.message(NewExpenses.category)
async def state_category_expenses(message: types.Message, state: FSMContext):
    await state.set_state(NewExpenses.quantity)
    if message.text in [i[0] for i in db.select_expenses()] or message.text == '🔙 Назад':
        if message.text == '🔙 Назад':
            await message.answer('Действие отменено',
                                 reply_markup=main_kb())
            await state.clear()
        else:
            if sub_categories(message.text).__len__() == 0:
                await message.answer('Введите сумму:\n'
                                     'Пример: 20000',
                                     reply_markup=back_btn())
                await state.update_data(sub_category='None')
                await state.update_data(category=message.text)
            else:
                await message.answer('Выберите подкатегорию',
                                     reply_markup=subcategory_types(message.text))
                await state.update_data(category=message.text)
                await state.set_state(NewExpenses.sub_category)
    else:
        await message.answer('Такой категории нет, выберите существующую')
        await state.set_state(NewExpenses.category)


@expenses_router.message(NewExpenses.sub_category)
async def state_sub_category_expenses(message: types.Message, state: FSMContext):
    st = await state.get_data()
    if message.text in [i[0] for i in db.select_subcategory(category_title=st['category'])] or message.text == '🔙 Назад':
        if message.text == '🔙 Назад':
            await message.answer('Выберите категорию',
                                 reply_markup=expense_types())
            await state.set_state(NewExpenses.category)
        else:
            await state.update_data(sub_category=message.text)
            await message.answer('Введите сумму:\n'
                                 'Пример: 20000',
                                 reply_markup=back_btn())
            await state.set_state(NewExpenses.quantity)
    else:
        await message.answer('Такой подкатегории нет, выберите существующую')
        await state.set_state(NewExpenses.sub_category)


@expenses_router.message(NewExpenses.quantity)
async def state_quantity_expenses(message: types.Message, state: FSMContext):
    if message.text == '🔙 Назад':
        await message.answer('Выберите категорию', reply_markup=expense_types())
        await state.set_state(NewExpenses.category)
    else:
        try:
            quantity = int(message.text)
            if isinstance(quantity, int):
                await message.answer('Выберите тип оплаты', reply_markup=income_types())
                await state.update_data(quantity=message.text)
                await state.set_state(NewExpenses.cart_name)
        except ValueError:
            await message.answer('Введите сумму корректно -> 20000')
            await state.set_state(NewExpenses.quantity)


@expenses_router.message(NewExpenses.cart_name)
async def state_cart_expenses(message: types.Message, state: FSMContext):
    if message.text in [i[0] for i in db.select_incomes()] or message.text == '🔙 Назад':
        if message.text == '🔙 Назад':
            await message.answer('Выберите категорию',
                                 reply_markup=expense_types())
            await state.set_state(NewExpenses.category)
        else:
            await message.answer('Введите описание',
                                 reply_markup=back_btn())

            await state.update_data(cart=message.text)
            await state.set_state(NewExpenses.description)
    else:
        await message.answer('Такого типа оплаты нет, выберите существующую')
        await state.set_state(NewExpenses.cart_name)


@expenses_router.message(NewExpenses.description)
async def state_description_expenses(message: types.Message, state: FSMContext):
    description = message.text
    if description == '🔙 Назад':
        await message.answer('Выберите тип оплаты', reply_markup=income_types())
        await state.set_state(NewExpenses.cart_name)
    else:
        await state.update_data(description=description)
        st = await state.get_data()
        if st['sub_category'] == 'None':
            await message.answer(f'<b>Расход:</b>\n\n'
                                 f'<b>Cумма:</b> {st["quantity"]}\n'
                                 f'<b>Валюта:</b> {st["uzs_usd"]}\n'
                                 f'<b>Категория:</b> {st["category"]}\n'
                                 f'<b>Подкатегория:</b> ❌\n'
                                 f'<b>Тип оплаты:</b> {st["cart"]}\n'
                                 f'<b>Описание:</b> {st["description"]}',
                                 reply_markup=accept_transactions())
        else:
            await message.answer(f'<b>Расход:</b>\n\n'
                                 f'<b>Cумма:</b> {st["quantity"]}\n'
                                 f'<b>Валюта:</b> {st["uzs_usd"]}\n'
                                 f'<b>Категория:</b> {st["category"]}\n'
                                 f'<b>Подкатегория:</b> {st["sub_category"]}\n'
                                 f'<b>Тип оплаты:</b> {st["cart"]}\n'
                                 f'<b>Описание:</b> {st["description"]}',
                                 reply_markup=accept_transactions())
        await state.set_state(NewExpenses.accept)


@expenses_router.message(NewExpenses.accept)
async def state_accept_expenses(message: types.Message, state: FSMContext):
    st = await state.get_data()
    if message.text == 'Подтвердить':
        await state.clear()
        user_id = message.chat.id
        type_title = 'expenses'
        quantity = st['quantity']
        description = st['description']
        expense_type = st['category']
        expense_subcategory = st['sub_category']
        income_type = st['cart']
        currency = st['uzs_usd']
        db.insert_transaction_expenses(user_id,
                                       type_title,
                                       quantity,
                                       description,
                                       income_type,
                                       expense_type,
                                       expense_subcategory,
                                       currency)
        await message.answer('Действие подтверждено', reply_markup=main_kb())
        db_quantity = db.select_quantity(category=f'"{income_type}"', telegram_id=user_id)[0]
        insert_quantity = int(db_quantity) - int(quantity)
        db.change_quantity(category=f'"{income_type}"', telegram_id=user_id, quantity=insert_quantity)
    elif message.text == 'Отменить':
        await state.clear()
        await message.answer('Действие отменено', reply_markup=main_kb())
    else:
        await message.answer('Выберите действие', reply_markup=accept_transactions())
        await state.set_state(NewExpenses.accept)


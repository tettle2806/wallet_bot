import hashlib

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.data.loader import db
from tg_bot.keyboards.reply import back_btn, main_kb, currency_btn, conversion_usd_btn, conversion_uzs_btn, \
    accept_transactions
from tg_bot.states.conversion_state import ConversionState

conversion_router = Router()


@conversion_router.message(F.text == '♻️Конвертация')
async def convert(message: Message, state: FSMContext):
    await message.answer('Введите пароль:', reply_markup=back_btn())
    await state.set_state(ConversionState.password)


@conversion_router.message(ConversionState.password)
async def password_state(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == '🔙 Назад':
        await message.answer('Действие отменено', reply_markup=main_kb())
        await state.clear()
    else:
        if db.select_password(chat_id)[0] == hashlib.sha256(message.text.encode('utf-8')).hexdigest():
            await message.answer('Выберите пару:', reply_markup=currency_btn())
            await state.set_state(ConversionState.currency_pair)
        else:
            await message.answer('Не верный пароль, введите правильный пароль', reply_markup=back_btn())
            await state.set_state(ConversionState.password)


def usd_balance(chat_id):
    db_balance = db.get_user_by_id(chat_id)
    return (f'<b>Наличные доллары:</b> ➡️  {db_balance[4]}\n'
            f'<b>Карта валютный (USD) 1:</b> ➡️  {db_balance[5]}\n'
            f'<b>Карта валютный (USD) 2:</b> ➡️  {db_balance[7]}\n'
            f'<b>Карта валютный (USD) 3:</b> ➡️  {db_balance[8]}\n'
            f'<b>Карта валютный (USD) 4:</b> ➡️  {db_balance[9]}\n')


def uzs_balance(chat_id):
    db_balance = db.get_user_by_id(chat_id)
    return (f'<b>Наличные сумы:</b> ➡️  {db_balance[3]}\n'
            f'<b>Карта суммовой (UZS) 1:</b> ➡️  {db_balance[6]}\n'
            f'<b>Карта суммовой (UZS) 2:</b> ➡️  {db_balance[10]}\n'
            f'<b>Карта суммовой (UZS) 3:</b> ➡️  {db_balance[11]}\n'
            f'<b>Карта суммовой (UZS) 4:</b> ➡️  {db_balance[12]}\n')


@conversion_router.message(ConversionState.currency_pair)
async def currency_state(message: Message, state: FSMContext):
    chat_id = message.chat.id
    currency_pair = message.text
    if currency_pair == '🔙 Назад':
        await message.answer('Действие отменено', reply_markup=main_kb())
        await state.clear()
    elif currency_pair in ['UZS ➡️ USD', 'USD ➡️ UZS']:
        if currency_pair == 'USD ➡️ UZS':
            await message.answer(usd_balance(chat_id), reply_markup=conversion_usd_btn())
            await state.update_data(currency_pair=currency_pair)
            await state.set_state(ConversionState.wallet_sender)
        elif currency_pair == 'UZS ➡️ USD':
            await message.answer(uzs_balance(chat_id), reply_markup=conversion_uzs_btn())
            await state.update_data(currency_pair=currency_pair)
            await state.set_state(ConversionState.wallet_sender)
    else:
        await message.answer('Выберите из предложенных вариантов')
        await state.set_state(ConversionState.currency_pair)


@conversion_router.message(ConversionState.wallet_sender)
async def wallet_sender_state(message: Message, state: FSMContext):
    wallet_sender = message.text
    chat_id = message.chat.id
    if wallet_sender == '🔙 Назад':
        await state.set_state(ConversionState.currency_pair)
        await message.answer('Выберите пару:', reply_markup=currency_btn())
    elif wallet_sender in [i[0] for i in db.select_incomes()]:
        currency_pair = await state.get_data()
        if currency_pair['currency_pair'] == 'USD ➡️ UZS':
            if wallet_sender in [i[0] for i in db.select_incomes_by_currency('usd')]:
                await message.answer('Выберите куда конвертировать деньги')
                await message.answer(uzs_balance(chat_id), reply_markup=conversion_uzs_btn())
                await state.update_data(wallet_sender=wallet_sender)
                await state.set_state(ConversionState.wallet_receive)
            else:
                await message.answer('Не существующая категория, выберите из предложенных')
                await state.set_state(ConversionState.wallet_sender)
        elif currency_pair['currency_pair'] == 'UZS ➡️ USD':
            if wallet_sender in [i[0] for i in db.select_incomes_by_currency('uzs')]:
                await message.answer('Выберите куда конвертировать деньги')
                await message.answer(usd_balance(chat_id), reply_markup=conversion_usd_btn())
                await state.update_data(wallet_sender=wallet_sender)
                await state.set_state(ConversionState.wallet_receive)
            else:
                await message.answer('Не существующая категория, выберите из предложенных')
                await state.set_state(ConversionState.wallet_sender)
    else:
        await message.answer('Не существующая категория, выберите из предложенных')
        await state.set_state(ConversionState.wallet_sender)


@conversion_router.message(ConversionState.wallet_receive)
async def wallet_receive_state(message: Message, state: FSMContext):
    wallet_receive = message.text
    chat_id = message.chat.id
    currency_pair = await state.get_data()
    if wallet_receive == '🔙 Назад':
        if currency_pair['currency_pair'] == 'USD ➡️ UZS':
            await message.answer(usd_balance(chat_id), reply_markup=conversion_usd_btn())
            await state.set_state(ConversionState.wallet_sender)
        elif currency_pair['currency_pair'] == 'UZS ➡️ USD':
            await message.answer(uzs_balance(chat_id), reply_markup=conversion_uzs_btn())
            await state.set_state(ConversionState.wallet_sender)
    elif wallet_receive in [i[0] for i in db.select_incomes()]:
        if currency_pair['currency_pair'] == 'USD ➡️ UZS':
            if wallet_receive in [i[0] for i in db.select_incomes_by_currency('uzs')]:

                await message.answer('Введите курс одного $', reply_markup=back_btn())
                await state.update_data(wallet_receive=wallet_receive)
                await state.set_state(ConversionState.pair_well)

            else:
                await message.answer('Не существующая категория, выберите из предложенных')
                await state.set_state(ConversionState.wallet_receive)
        elif currency_pair['currency_pair'] == 'UZS ➡️ USD':
            if wallet_receive in [i[0] for i in db.select_incomes_by_currency('usd')]:

                await message.answer('Введите курс одного $', reply_markup=back_btn())
                await state.update_data(wallet_receive=wallet_receive)
                await state.set_state(ConversionState.pair_well)

            else:
                await message.answer('Не существующая категория, выберите из предложенных')
                await state.set_state(ConversionState.wallet_receive)

    else:
        await message.answer('Не существующая категория, выберите из предложенных')
        await state.set_state(ConversionState.wallet_receive)


@conversion_router.message(ConversionState.pair_well)
async def quantity_state(message: Message, state: FSMContext):
    pair_well = message.text
    currency_pair = await state.get_data()
    chat_id = message.chat.id
    if pair_well == '🔙 Назад':
        if currency_pair['currency_pair'] == 'USD ➡️ UZS':
            await message.answer(uzs_balance(chat_id), reply_markup=conversion_uzs_btn())
            await state.set_state(ConversionState.wallet_sender)
        elif currency_pair['currency_pair'] == 'UZS ➡️ USD':
            await message.answer(usd_balance(chat_id), reply_markup=conversion_usd_btn())
            await state.set_state(ConversionState.wallet_sender)
    else:
        try:
            int_pair_well = int(pair_well)
            await message.answer('Введите сумму конвертации в $', reply_markup=back_btn())
            await state.update_data(pair_well=pair_well)
            await state.set_state(ConversionState.quantity)
        except ValueError:
            await message.answer('Не верный формат введите число')
            await state.set_state(ConversionState.pair_well)


@conversion_router.message(ConversionState.quantity)
async def quantity_state(message: Message, state: FSMContext):
    quantity = message.text
    chat_id = message.chat.id
    state_info = await state.get_data()
    if quantity == '🔙 Назад':
        await message.answer('Введите курс одного $')
        await state.set_state(ConversionState.pair_well)
    else:
        pair_well = int(state_info['pair_well'])
        sum_uzs = int(pair_well) * int(quantity)
        quantity_sender_wallet = db.select_quantity(f'"{state_info['wallet_sender']}"', chat_id)
        if state_info['currency_pair'] == 'USD ➡️ UZS':
            if int(quantity) > int(quantity_sender_wallet[0]):
                await message.answer(
                    f'Сумма конвертации превышает сумму на кошельке <b>{state_info['wallet_sender']}</b>')
                await message.answer('Введите сумму конвертации в $', reply_markup=back_btn())
                await state.set_state(ConversionState.quantity)
            else:

                await message.answer(f'<b>Конвертация:</b> {state_info["currency_pair"]}\n'
                                     f'<b>Кошелек отправления:</b> {state_info["wallet_sender"]}\n'
                                     f'<b>Кошелек получения:</b> {state_info["wallet_receive"]}\n'
                                     f'<b>Курс:</b> {state_info["pair_well"]}\n'
                                     f'<b>Сумма в $:</b> {quantity}', reply_markup=accept_transactions())
                await state.update_data(quantity=quantity)
                await state.set_state(ConversionState.accept)

        elif state_info['currency_pair'] == 'UZS ➡️ USD':
            if sum_uzs > int(quantity_sender_wallet[0]):
                await message.answer(
                    f'Сумма конвертации превышает сумму на кошельке <b>{state_info['wallet_sender']}</b>')
                await message.answer('Введите сумму конвертации в $', reply_markup=back_btn())
                await state.set_state(ConversionState.quantity)
            else:

                await message.answer(f'<b>Конвертация:</b> {state_info["currency_pair"]}\n'
                                     f'<b>Кошелек отправления:</b> {state_info["wallet_sender"]}\n'
                                     f'<b>Кошелек получения:</b> {state_info["wallet_receive"]}\n'
                                     f'<b>Курс:</b> {state_info["pair_well"]}\n'
                                     f'<b>Сумма в $:</b> {quantity}', reply_markup=accept_transactions())
                await state.update_data(quantity=quantity)
                await state.set_state(ConversionState.accept)


@conversion_router.message(ConversionState.accept)
async def accept_state(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == 'Подтвердить':
        state_info = await state.get_data()
        quantity_sender_wallet = db.select_quantity(f'"{state_info['wallet_sender']}"', chat_id)
        quantity_receive = db.select_quantity(f'"{state_info['wallet_receive']}"', chat_id)
        if state_info['currency_pair'] == 'USD ➡️ UZS':
            save_quantity_sender1 = int(quantity_sender_wallet[0]) - int(state_info['quantity']) # доллары
            save_quantity_receive1 = int(quantity_receive[0]) + (int(state_info['quantity']) * int(state_info['pair_well'])) # сумы
            db.conversion_update(f'"{state_info['wallet_sender']}"', chat_id, save_quantity_sender1)
            db.conversion_update(f'"{state_info['wallet_receive']}"', chat_id, save_quantity_receive1)
            await message.answer('Операция прошла успешно', reply_markup=main_kb())
            await state.clear()
        elif state_info['currency_pair'] == 'UZS ➡️ USD':
            save_quantity_sender2 = int(quantity_sender_wallet[0]) - (int(state_info['quantity']) * int(state_info['pair_well']))
            save_quantity_receive2 = int(quantity_receive[0]) + int(state_info['quantity'])
            db.conversion_update(f'"{state_info['wallet_sender']}"', chat_id, save_quantity_sender2)
            db.conversion_update(f'"{state_info['wallet_receive']}"', chat_id, save_quantity_receive2)
            await message.answer('Операция прошла успешно', reply_markup=main_kb())
            await state.clear()
    elif message.text == 'Отменить':
        await state.clear()
        await message.answer('Действие отменено', reply_markup=main_kb())
        await state.clear()
    else:
        await message.answer('Выберите действие', reply_markup=accept_transactions())
        await state.set_state(ConversionState.accept)
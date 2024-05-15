from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from tg_bot.data.loader import db


def main_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='➕ Доходы'),
            KeyboardButton(text='➖ Расходы')
        ],
        [
            KeyboardButton(text='♻️Конвертация')
        ],
        [
            KeyboardButton(text='📈Аналитика')
        ],
        [
            KeyboardButton(text='⚙️Настройки')
        ]
    ], row_width=2)
    return markup


def generate_categories(categories: list):
    buttons = []
    for category in categories:
        btn = KeyboardButton(text=category)
        buttons.append(btn)
    back = KeyboardButton(text='🔙 Назад')
    buttons.append(back)
    result = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=result)
    return markup


def income_types():
    categories = [i[0] for i in db.select_incomes()]
    return generate_categories(categories)


def expense_types():
    categories = [i[0] for i in db.select_expenses()]
    return generate_categories(categories)


def conversion_usd_btn():
    categories = [i[0] for i in db.select_incomes_by_currency('usd')]
    return generate_categories(categories)


def conversion_uzs_btn():
    categories = [i[0] for i in db.select_incomes_by_currency('uzs')]
    return generate_categories(categories)

def subcategory_types(category):
    categories = [i[0] for i in db.select_subcategory(category)]
    if categories.__len__() == 0:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [
                KeyboardButton(text='🔙 Назад')
            ]
        ])
        return markup
    else:
        return generate_categories(categories)


def accept_transactions():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Подтвердить'),
            KeyboardButton(text='Отменить')
        ]
    ])
    return markup


def back_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, is_persistent=True, keyboard=[
        [
            KeyboardButton(text='🔙 Назад')
        ]
    ])
    return markup


def menu_statistics():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Баланс')
        ],
        [
            KeyboardButton(text='Доходы'),
            KeyboardButton(text='Расходы')
        ],
        [
            KeyboardButton(text='Транзакции'),
            KeyboardButton(text='🔙 Назад')
        ]
    ])
    return markup


def uzs_usd_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='UZS'),
            KeyboardButton(text='USD')
        ],
        [
            KeyboardButton(text='🔙 Назад')
        ]
    ])
    return markup


def currency_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='UZS ➡️ USD'),
            KeyboardButton(text='USD ➡️ UZS')
        ],
        [
            KeyboardButton(text='🔙 Назад')
        ]
    ])
    return markup


def setting_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='🗑️ Очистить транзакции')
        ],
        [
            KeyboardButton(text='☢️ Изменить пароль')
        ],
        [
            KeyboardButton(text='🔙 Назад')
        ]
    ])
    return markup

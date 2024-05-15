import datetime

from tg_bot.data.config import DB_PATH, TRANSACTION_PATH
from tg_bot.data.loader import db
from tg_bot.files.analytics import transactions
from tg_bot.handlers.users.conversion import usd_balance
from tg_bot.keyboards.reply import income_types

# db.drop_incomes_types()
# db.drop_expenses_subcategory()
# db.drop_expenses()
# db.drop_transactions()
# db.drop_user_table()

# db.create_user_table()
# db.create_incomes_types()
# db.create_expenses_types()
# db.create_expenses_subcategory()
# db.create_transactions()

# db.insert_user('237888590')
# db.insert_user('660515831')
# db.insert_incomes_types()
# db.insert_expenses_types()
# db.insert_expenses_subcategory()

# db.expenses_quantity("'Наличные доллары'", 660515831, '100')

# print(db.select_quantity('"Наличные доллары"', 660515831))
# transactions(5488702955)
# print(TRANSACTION_PATH)

# print(db.select_password('660515831'))

# db.insert_password('660515831', password='<PASSWORD>')
# print(db.get_user_by_id('660515831'))

# print(db.select_balance('660515831'))

# print(db.select_count_of_expenses()[0][0])
# print(db.select_count_of_incomes()[0][0])
# print(db.select_usd_income_nal())
# print(db.select_usd_income())
# db.insert_transaction_income('660515831', 'income', 150, 'text', 'asd', 'USD')

# print(usd_balance(660515831))

db.conversion_update('"Наличные доллары"', 660515831, 300)

import sqlite3


class DataBase:
    def __init__(self):
        self.database = sqlite3.connect('acc.db', check_same_thread=False)

    def manager(self, sql: object, *args: object,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False) -> object:
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result

    def create_user_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id BIGINT INTEGER,
            password VARCHAR(255),
            'Наличные сумы' INTEGER DEFAULT 0,
            'Наличные доллары' INTEGER DEFAULT 0,
            'Карта валютный (USD) 1' INTEGER DEFAULT 0,
            'Карта суммовой (UZS) 1' INTEGER DEFAULT 0,
            'Карта валютный (USD) 2' INTEGER DEFAULT 0,
            'Карта валютный (USD) 3' INTEGER DEFAULT 0,
            'Карта валютный (USD) 4' INTEGER DEFAULT 0,
            'Карта суммовой (UZS) 2' INTEGER DEFAULT 0,
            'Карта суммовой (UZS) 3' INTEGER DEFAULT 0,
            'Карта суммовой (UZS) 4' INTEGER DEFAULT 0
            )
        '''
        self.manager(sql, commit=True)

    def select_password(self, telegram_id):
        sql = '''
            SELECT password FROM users WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def insert_password(self, telegram_id, password):
        sql = '''
            UPDATE users SET password = ? WHERE telegram_id = ?
        '''
        self.manager(sql, password, telegram_id, commit=True)

    def conversion_update(self, wallet, telegram_id, quantity):
        sql = f'''
            UPDATE users 
            SET {wallet} = {quantity} 
            WHERE telegram_id = ?
        '''
        self.manager(sql, telegram_id, commit=True)


    def drop_user_table(self):
        sql = '''
            DROP TABLE IF EXISTS users
        '''
        self.manager(sql, commit=True)

    def get_user_by_id(self, telegram_id):
        sql = '''
            SELECT * FROM users WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def insert_user(self, telegram_id):
        sql = '''
            INSERT INTO users(telegram_id) VALUES (?)
            '''
        self.manager(sql, telegram_id, commit=True)

    def delete_user(self, telegram_id):
        sql = '''
            DELETE FROM users WHERE telegram_id = ?
        '''
        self.manager(sql, telegram_id, commit=True)

    def create_incomes_types(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS incomes(
            type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_title VARCHAR(50) UNIQUE,
            currency VARCHAR(3)
        )
        '''
        self.manager(sql, commit=True)

    def drop_incomes_types(self):
        sql = '''
            DROP TABLE IF EXISTS incomes
        '''
        self.manager(sql, commit=True)

    def insert_incomes_types(self):
        sql = '''
            INSERT INTO incomes(type_title, currency) VALUES
            ('Наличные сумы', 'uzs'),
            ('Наличные доллары', 'usd'),    
            ('Карта валютный (USD) 1', 'usd'),    
            ('Карта суммовой (UZS) 1', 'uzs'),    
            ('Карта валютный (USD) 2', 'usd'),    
            ('Карта валютный (USD) 3', 'usd'),   
            ('Карта валютный (USD) 4', 'usd'),    
            ('Карта суммовой (UZS) 2', 'uzs'),    
            ('Карта суммовой (UZS) 3', 'uzs'),
            ('Карта суммовой (UZS) 4', 'uzs')    
            '''
        self.manager(sql, commit=True)

    def select_incomes_by_currency(self, currency):
        sql = '''
            SELECT type_title FROM incomes WHERE currency = ?
        '''
        return self.manager(sql, currency, fetchall=True)


    def change_quantity(self, category, telegram_id, quantity):
        sql = f'''
            UPDATE users 
            SET {category} = ? 
            WHERE telegram_id = ?
        '''
        self.manager(sql, quantity, telegram_id, commit=True)

    def select_quantity(self, category, telegram_id):
        sql = f'''
            SELECT {category} FROM users WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)


    def create_expenses_types(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS expenses(
        type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_title VARCHAR(50) UNIQUE
        )'''
        self.manager(sql, commit=True)

    def drop_expenses(self):
        sql = '''
            DROP TABLE IF EXISTS expenses
        '''
        self.manager(sql, commit=True)

    def insert_expenses_types(self):
        sql = '''
            INSERT INTO expenses(type_title) VALUES
            ('Без категории'),
            ('Автомобиль'),
            ('$ Банк'),
            ('Благотворительность'),
            ('Государство'),
            ('Дети'),
            ('Дом'),
            ('Домашние животные'),
            ('Другое'),
            ('Еда вне дома'),
            ('Здоровье'),
            ('Красота'),
            ('Мобильная связь'),
            ('Образование'),
            ('Одежда и обувь'),
            ('Подарки'),
            ('Продукты питания'),
            ('Путешествия'),
            ('Развлечения'),
            ('Техника'),
            ('Транспорт')
        '''
        self.manager(sql, commit=True)

    def create_expenses_subcategory(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS expenses_subcategory(
            subcategory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subcategory_title VARCHAR(50) UNIQUE,
            expenses_type INTEGER REFERENCES expenses_types(type_id)
            )
        '''
        self.manager(sql, commit=True)

    def insert_expenses_subcategory(self):
        sql = '''
            INSERT INTO expenses_subcategory(subcategory_title, expenses_type) VALUES
            ('Автохимия', 2),
            ('Аксессуары машины', 2),
            ('Запчасти', 2),
            ('Мойка', 2),
            ('Парковка', 2),
            ('Платные дороги', 2),
            ('Сервис', 2),
            ('Страховка машины', 2),
            ('Топливо', 2),
            ('Бизнес-услуги', 3),
            ('Налоги', 5),
            ('Пошлины', 5),
            ('Штрафы', 5),
            ('Занятия', 6),
            ('Здоровье', 6),
            ('Игрушки', 6),
            ('Одежда', 6),
            ('Питание', 6),
            ('Аренда', 7),
            ('Бытовая химия', 7),
            ('Бытовые услуги', 7),
            ('Газ', 7),
            ('Интернет', 7),
            ('Квартплата', 7),
            ('Мебель', 7),
            ('Посуда', 7),
            ('Ремонт', 7),
            ('Страхование', 7),
            ('Телефон', 7),
            ('Электричество', 7),
            ('Аксессуары, игрушки', 8),
            ('Вет. услуги', 8),
            ('Корм', 8),
            ('Медикаменты', 8),
            ('Кофейня', 10),
            ('Ланч', 10),
            ('Ресторан', 10),
            ('Фастфуд', 10),
            ('Аптека', 11),
            ('Инвентарь', 11),
            ('Мед. услуги', 11),
            ('Спорт', 11),
            ('Страхование здоровья', 11),
            ('Косметика', 12),
            ('Стрижка', 12),
            ('Книги', 14),
            ('Услуги', 14),
            ('Аксессуары', 15),
            ('Взрослая', 15),
            ('Детская', 15),
            ('Аренда авто', 18),
            ('Билеты', 18),
            ('Визы', 18),
            ('Отель', 18),
            ('Страховка', 18),
            ('Сувениры', 18),
            ('Услуги путешествие', 18),
            ('Бытовая техника', 20),
            ('Электроника', 20),
            ('Такси', 21),
            ('Метро', 21),
            ('Автобус', 21),
            ('Трамвай', 21)
        '''
        self.manager(sql, commit=True)

    def drop_expenses_subcategory(self):
        sql = '''
            DROP TABLE IF EXISTS expenses_subcategory
        '''
        self.manager(sql, commit=True)

    def create_transactions(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(telegram_id),
            type_title VARCHAR(50),
            quantity INTEGER NOT NULL,
            description VARCHAR(50),
            income_type VARCHAR REFERENCES incomes(type_title),
            expenses_type VARCHAR REFERENCES expenses(type_title),
            expenses_subcategory INTEGER REFERENCES expenses_subcategory(subcategory_title),
            uzs_usd VARCHAR(5),
            created_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
            )
        '''
        self.manager(sql, commit=True)

    def drop_transactions(self):
        sql = '''
            DROP TABLE IF EXISTS transactions
        '''
        self.manager(sql, commit=True)

    def select_incomes(self):
        sql = '''
            SELECT type_title FROM incomes
        '''
        return self.manager(sql, fetchall=True)

    def select_expenses(self):
        sql = '''
            SELECT type_title FROM expenses
        '''
        return self.manager(sql, fetchall=True)

    def select_subcategory(self, category_title):
        sql = '''
                    SELECT subcategory_title FROM expenses_subcategory WHERE expenses_type = (
                        SELECT type_id FROM expenses WHERE type_title = ?
                    )
                '''
        return self.manager(sql, category_title, fetchall=True)

    def insert_transaction_income(self, user_id, type_title, quantity, description, income_type, uzs_usd):
        sql = '''
            INSERT INTO transactions(user_id, type_title, quantity, description, income_type, uzs_usd) VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.manager(sql, user_id, type_title, quantity, description, income_type, uzs_usd, commit=True)

    def insert_transaction_expenses(self, user_id, type_title, quantity, description, income_type, expenses_type,
                                    expenses_subcategory, uzs_usd):
        sql = '''
            INSERT INTO transactions(user_id, type_title, quantity, description, income_type, expenses_type, expenses_subcategory, uzs_usd) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.manager(sql, user_id, type_title, quantity, description, income_type, expenses_type, expenses_subcategory,
                     uzs_usd, commit=True)

    def select_count_of_expenses(self):
        sql = '''
        SELECT COUNT(*) FROM transactions WHERE type_title = ('expenses')
        '''
        return self.manager(sql, fetchall=True)

    def select_count_of_incomes(self):
        sql = '''
            SELECT COUNT(*) FROM transactions WHERE type_title = ('income')
        '''
        return self.manager(sql, fetchall=True)

    def select_usd_income(self, telegram_id):
        sql = '''
            SELECT SUM(quantity) FROM transactions WHERE type_title = ('income') AND uzs_usd = ('USD') AND user_id = ?
        '''
        return self.manager(sql, telegram_id, fetchall=True)

    def select_uzs_income(self, telegram_id):
        sql = '''
            SELECT SUM(quantity) FROM transactions WHERE type_title = ('income') AND uzs_usd = ('UZS') AND user_id = ?
        '''
        return self.manager(sql,telegram_id, fetchall=True)

    def select_usd_expenses(self, telegram_id):
        sql = '''
            SELECT SUM(quantity) FROM transactions WHERE type_title = ('expenses') AND uzs_usd = ('USD') AND user_id = ?
        '''
        return self.manager(sql, telegram_id, fetchall=True)

    def select_uzs_expenses(self, telegram_id):
        sql = '''
            SELECT SUM(quantity) FROM transactions WHERE type_title = ('expenses') AND uzs_usd = ('UZS') AND user_id = ?
        '''
        return self.manager(sql, telegram_id, fetchall=True)

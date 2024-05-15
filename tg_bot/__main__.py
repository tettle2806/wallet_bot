import asyncio
import logging

import sys
from tg_bot.data.config import set_commands, ADMINS
from tg_bot.data.loader import bot, dp
from tg_bot.files.analytics import analytics_router
from tg_bot.handlers.admin.bot_start import admin_notify
from tg_bot.handlers.users.add_expenses import expenses_router
from tg_bot.handlers.users.add_incomes import add_income_router
from tg_bot.handlers.users.conversion import conversion_router
from tg_bot.handlers.users.setting import settings_router
from tg_bot.handlers.users.start import start_router
from tg_bot.handlers.admin.add_new_user import admin_router


async def main():
    await set_commands(bot)
    await admin_notify(bot)
    dp.include_router(add_income_router)
    dp.include_router(expenses_router)
    dp.include_router(conversion_router)
    dp.include_router(settings_router)
    dp.include_router(analytics_router)
    dp.include_router(start_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')

import asyncio
import os
from loader import dp,bot,db
from aiogram import types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import logging

import middlewares, filters, handlers

from data import config
#from data import debug_config as config

from aiogram.utils.executor import start_webhook
"""
from bot.postgres import PostgreSQL #расскоментить при загрузке на прод
from bot.games import whatWhereWhen as www #расскоментить при загрузке на прод
from bot.settings import (BOT_TOKEN, HEROKU_APP_NAME, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, ADMIN_ID,BOT_ID) #расскоментить при загрузке на прод
"""

#"""
#from debug_config import (BOT_TOKEN, ADMIN_ID, BOT_ID) #расскоментить при зтестировании
from aiogram.utils import executor #расскоментить при зтестировании
#"""



logging.basicConfig(level=logging.DEBUG)



user = None
logging.info(f'НАЧАЛО ПРОГРАММЫ')



async def on_startup(dp):
    logging.warning(
        'Установка Вебхука')
    await bot.set_webhook(config.WEBHOOK_URL,drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Выключение Вебхука')


logging.info(f'САМЫЙ КОНЕЦ ПРОГРАММЫ')



#if '__init__' == '__main__':
#executor.start_polling(dp, on_startup=on_startup)




def main():
    logging.basicConfig(level=logging.INFO)

    start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        #loop=lo,
        skip_updates=True,
        on_startup=on_startup,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT,
    )


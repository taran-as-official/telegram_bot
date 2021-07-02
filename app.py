from loader import dp,bot

import logging
import middlewares, filters, handlers #не уда

from data import config
#from data import debug_config as config

from aiogram.utils.executor import start_webhook

from aiogram.utils import executor #расскоментить при зтестировании
import  asyncio



user = None
logging.debug(f'НАЧАЛО ПРОГРАММЫ')



async def on_startup(dp):
    logging.warning(
        'Установка Вебхука')
    await bot.set_webhook(config.WEBHOOK_URL,drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Выключение Вебхука')


logging.info(f'САМЫЙ КОНЕЦ ПРОГРАММЫ')



#if '__init__' == '__main__':
#executor.start_polling(dp, on_startup=on_startup,loop=asyncio.get_event_loop())

#executor.start_polling(dp, on_startup=on_startup,loop=asyncio.get_event_loop())


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


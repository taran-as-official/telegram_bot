''' Run a function by ado <func_name> '''
from aiogram.utils.executor import start_webhook
from data import config
#from data import debug_config as config
import logging
from loader import dp,bot,db

logging.basicConfig(level=logging.DEBUG)

def set_hook():
    import asyncio
    from data.config import HEROKU_APP_NAME, WEBHOOK_URL, BOT_TOKEN
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)

    async def hook_set():
        if not HEROKU_APP_NAME:
            print('You have forgot to set HEROKU_APP_NAME')
            quit()
        await bot.set_webhook(WEBHOOK_URL)
        print('Какая та инфа по вебхуку: ' + await bot.get_webhook_info())
    

    asyncio.run(hook_set())
    bot.close()

"""
def start():
    import logging
    from bot import main
    try:
        main()
    except Exception:
       logging.exception()
"""

async def on_startup(dp):
    logging.warning(
        'Установка Вебхука')
    await bot.set_webhook(config.WEBHOOK_URL,drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Выключение Вебхука')


logging.info(f'САМЫЙ КОНЕЦ ПРОГРАММЫ')



#if '__init__' == '__main__':
#executor.start_polling(dp, on_startup=on_startup)




def start():
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


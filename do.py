''' Run a function by ado <func_name> '''


def set_hook():
    import asyncio
    from data.config import HEROKU_APP_NAME, WEBHOOK_URL, BOT_TOKEN
    from aiogram import Bot
    import logging
    bot = Bot(token=BOT_TOKEN)

    async def hook_set():
        if not HEROKU_APP_NAME:
            logging.info('Вы не становили параметр HEROKU_APP_NAME')
            quit()
        await bot.set_webhook(WEBHOOK_URL)
        logging.info('Какая та инфа по вебхуку: ' + await bot.get_webhook_info())
    

    asyncio.run(hook_set())
    bot.close()


def start():
    import logging
    from app import main
    try:
        main()
    except Exception:
       logging.exception()
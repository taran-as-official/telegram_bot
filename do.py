''' Run a function by ado <func_name> '''


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


def start():
    import logging
    from bot import main
    try:
        main()
    except Exception:
       logging.exception()
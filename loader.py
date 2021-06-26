from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.postgres import PostgreSQL #расскоментить при зтестировании

#from data import config
from data import debug_config as config




bot = Bot(token=config.BOT_TOKEN,parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)
db = PostgreSQL()

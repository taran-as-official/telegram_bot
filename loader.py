from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.postgres import PostgreSQL #расскоментить при зтестировании
#from utils.misc import logging
from data import config
#from data import debug_config as config
import logging

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    #level=logging.DEBUG  # Можно заменить на другой уровень логгирования.
                    #level=logging.WARNING
                    )


bot = Bot(token=config.BOT_TOKEN,parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)
db = PostgreSQL()

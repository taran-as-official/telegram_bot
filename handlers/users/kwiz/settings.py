from aiogram.types import CallbackQuery

from keyboards.inline import play_game
from loader import dp

@dp.callback_query_handler(text="kwiz")
async def settings_www_game_fnc(call: CallbackQuery):
    await call.answer("Игра еще в разработке",show_alert=False)


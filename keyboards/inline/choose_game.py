from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import play_game

choose_game = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Что? Где? Когда?', callback_data = "www")
        ],
        [
            InlineKeyboardButton(text='Квиз',callback_data = "kwiz")
        ]
    ]

)
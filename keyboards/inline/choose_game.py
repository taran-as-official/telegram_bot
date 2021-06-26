from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import play_game

choose_game = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Что? Где? Когда?', callback_data = play_game.new(
                game_name = "www",
                count_teams = 1
            ))
        ],
        [
            InlineKeyboardButton(text='Квиз',callback_data = play_game.new(
                game_name = "kwiz",
                count_teams = 1
            ))
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]

)
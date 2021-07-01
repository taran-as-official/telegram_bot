from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from keyboards.inline.callback_data import timer

countTeamsKeyMark = InlineKeyboardMarkup(
    inline_keyboard=[
        {
            InlineKeyboardButton(text="1", callback_data="1"),
            InlineKeyboardButton(text="2", callback_data="2"),
            InlineKeyboardButton(text="3", callback_data="3"),
            InlineKeyboardButton(text="4", callback_data="4")
        }
    ]
)



hostInfo = InlineKeyboardMarkup(
    inline_keyboard=[
        {
            InlineKeyboardButton(text="Буду играть", callback_data="1"),
            InlineKeyboardButton(text="Буду ведущим", callback_data="0")
        }
    ]
)



start_game = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Начать игру', callback_data = "start_game")
        ]
    ]

)

give_minute = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Дать минуту', callback_data = "start_timer")
        ]
    ]

)

#досрочный ответ
early_answer = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Досрочный ответ', callback_data = "stop_timer")
        ]
    ]

)

#средующий вопрос
next_question = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Далее', callback_data = "next_question"),
            InlineKeyboardButton(text='Выход', callback_data = "exit")
        ]
    ]

)

#средующий вопрос
exit_game = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Выход', callback_data = "exit")
        ]
    ]

)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from keyboards.inline.callback_data import timer

give_minute = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Дать минуту', callback_data = timer.new(seconds = 60))
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
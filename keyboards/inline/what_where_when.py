from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from keyboards.inline.callback_data import timer
#этот способ не используем потому что кнопки постоянно в другом порядке
"""
countTeamsKeyMark = InlineKeyboardMarkup(
    inline_keyboard=[
        {
            InlineKeyboardButton(text="1", callback_data="1"),
            InlineKeyboardButton(text="2", callback_data="2"),
            InlineKeyboardButton(text="3", callback_data="3"),
            InlineKeyboardButton(text="4", callback_data="4"),
            InlineKeyboardButton(text="5", callback_data="5")

        },
        {
            InlineKeyboardButton(text="6", callback_data="6"),
            InlineKeyboardButton(text="7", callback_data="7"),
            InlineKeyboardButton(text="8", callback_data="8"),
            InlineKeyboardButton(text="9", callback_data="9"),
            InlineKeyboardButton(text="10", callback_data="10")

        }
    ]
)
"""

countTeamsKeyMark = InlineKeyboardMarkup()

countTeams1 = InlineKeyboardButton(text="1", callback_data="1")
countTeams2 = InlineKeyboardButton(text="2", callback_data="2")
countTeams3 = InlineKeyboardButton(text="3", callback_data="3")
countTeams4 = InlineKeyboardButton(text="4", callback_data="4")
countTeams5 = InlineKeyboardButton(text="5", callback_data="5")
countTeams6 = InlineKeyboardButton(text="6", callback_data="6")
countTeams7 = InlineKeyboardButton(text="7", callback_data="7")
countTeams8 = InlineKeyboardButton(text="8", callback_data="8")
countTeams9 = InlineKeyboardButton(text="9", callback_data="9")
countTeams10 = InlineKeyboardButton(text="10", callback_data="10")


countTeamsKeyMark.row(countTeams1, countTeams2, countTeams3, countTeams4, countTeams5)
countTeamsKeyMark.row(countTeams6, countTeams7, countTeams8, countTeams9, countTeams10)

"""
hostInfo = InlineKeyboardMarkup(
    inline_keyboard=[
        {
            InlineKeyboardButton(text="Буду играть", callback_data="1"),
            InlineKeyboardButton(text="Буду ведущим", callback_data="0")
        }
    ]
)
"""

hostInfo = InlineKeyboardMarkup()

hostInfoBtn1 = InlineKeyboardButton(text="Буду играть", callback_data="1")
hostInfoBtn2 = InlineKeyboardButton(text="Буду ведущим", callback_data="0")

hostInfo.row(hostInfoBtn1, hostInfoBtn2)


connInGame = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Войти в игру', callback_data = "wait_teams")
        ]
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
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        {
            KeyboardButton(text='Да'),
            KeyboardButton(text='Нет')
        },
        [
            KeyboardButton(text='10'),
            KeyboardButton(text='20')
        ]
    ],
    resize_keyboard=True

)
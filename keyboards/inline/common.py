from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#выбор метода приглашения пользователей в игру
shareMethodMrp = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отправить ссылку', callback_data="send_link"),
            InlineKeyboardButton(text='Сканировать QR-code', callback_data="scan_qrcode")
        ]
    ]

)

shareLinkMrp = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Пригласить в игру',switch_inline_query="")
        ]
    ]

)

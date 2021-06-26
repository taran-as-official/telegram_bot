from aiogram.utils.callback_data import CallbackData

play_game = CallbackData("play", "game_name", "count_teams")
timer = CallbackData("start_timer", "seconds")
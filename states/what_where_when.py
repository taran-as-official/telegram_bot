from aiogram.dispatcher.filters.state import StatesGroup, State



class WhatWhereWhen(StatesGroup):
    getCountTeams = State()
    getHostInfo = State()
    getNameTeam = State()
    inviteTeam = State()
    getShareMethod = State()
    waitTeam = State()
    joinGame = State()
    readyPlay = State()
    leadGame = State() #вести игру
    answerPlayer = State() #отвечать на вопросы
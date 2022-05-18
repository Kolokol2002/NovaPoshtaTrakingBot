#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn = [
    KeyboardButton('✅Трекінг по ТТН'),
]

def_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,)
def_kb.add(*btn)


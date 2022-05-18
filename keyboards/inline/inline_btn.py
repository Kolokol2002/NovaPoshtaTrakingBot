#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_btn_back = InlineKeyboardButton('🔙Назад', callback_data='back')
inline_back = InlineKeyboardMarkup().add(inline_btn_back)


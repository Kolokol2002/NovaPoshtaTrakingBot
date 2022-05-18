#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiogram.dispatcher.filters.state import StatesGroup, State


class TTN(StatesGroup):
    ttn = State()
    minute = State()

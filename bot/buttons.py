from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from filters import vacancy_filters
from aiogram.filters.callback_data import CallbackData


def add_inline_filters():
    markup = InlineKeyboard()
    for key, value in vacancy_filters.items():
        markup.add(InlineKeyboardButton(text=value, callback_data=key))
    markup.add(InlineKeyboardButton(text="Search with selected filters", callback_data="apply"))
    return markup

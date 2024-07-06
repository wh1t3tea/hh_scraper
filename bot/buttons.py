from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters import vacancy_filters


def add_inline_filters():
    markup = InlineKeyboardBuilder()
    for key, value in vacancy_filters.items():
        markup.add(InlineKeyboardButton(text=value, callback_data=key))
    markup.add(InlineKeyboardButton(text="Search with selected filters", callback_data="apply"))
    return markup

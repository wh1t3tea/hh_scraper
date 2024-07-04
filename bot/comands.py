from aiogram import Bot
from aiogram.types import BotCommandScopeDefault, BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/parse", description="Start parsing from HH.ru"),
        BotCommand(command="/get_from_db", description="Get saved data"),
        BotCommand(command="/start", description="Main menu"),
        BotCommand(command="/analytics", description="Show short analytics for saved data")
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault()
    )

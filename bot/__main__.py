import asyncio
import os

from aiogram import Bot, Dispatcher

import handlers
from comands import set_commands

BOT_TOKEN = os.environ["BOT_TOKEN"]

API_route = os.environ["API_ROUTE"]


async def main():
    loop = asyncio.get_event_loop()

    bot = Bot(BOT_TOKEN)

    dp = Dispatcher()

    dp.include_router(handlers.callback_router)
    dp.include_router(handlers.state_router)
    dp.include_router(handlers.command_router)

    await set_commands(bot)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())

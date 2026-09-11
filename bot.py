import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import load_config
from handlers.application import router as application_router
from handlers.start import router as start_router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    config = load_config()
    bot = Bot(token=config.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    dp["config"] = config

    dp.include_router(start_router)
    dp.include_router(application_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass

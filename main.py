import logging
from datetime import datetime
from Scheduler import count_streaks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Dispatcher
from handlers import start, add_beverages, settings
from data import db_session
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from Bot import bot

storage = MemoryStorage()

dp = Dispatcher(storage=storage)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    db_session.global_init("data.db3")
    dp.include_routers(start.router, add_beverages.router, settings.router)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(count_streaks, trigger='interval', hours=1,
                      start_date=datetime.strptime('24:00', '%H:%M'))
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

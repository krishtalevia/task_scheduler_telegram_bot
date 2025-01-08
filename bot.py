import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import start, add_task, auth, view_tasks, edit_task, complete_task, delete_task, reminders, statistics, help
from reminder_scheduler import reminder_schedule
from model import init_db

async def main():
    bot = Bot(token=TOKEN) 
    dp = Dispatcher()

    init_db()

    dp.include_routers(start.router)
    dp.include_routers(auth.router)
    dp.include_routers(add_task.router)
    dp.include_routers(view_tasks.router)
    dp.include_routers(edit_task.router)
    dp.include_routers(complete_task.router)
    dp.include_routers(delete_task.router)
    dp.include_routers(reminders.router)
    dp.include_routers(statistics.router)
    dp.include_routers(help.router)

    reminder_task = asyncio.create_task(reminder_schedule(bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    await reminder_task

if __name__ == '__main__':
    asyncio.run(main())

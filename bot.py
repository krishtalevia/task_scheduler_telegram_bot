import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import start, add_task, auth, view_tasks, edit_task, complete_task

async def main():
    bot = Bot(token=TOKEN) 
    dp = Dispatcher()

    dp.include_routers(start.router)
    dp.include_routers(auth.router)
    dp.include_routers(add_task.router)
    dp.include_routers(view_tasks.router)
    dp.include_router(edit_task.router)
    dp.include_router(complete_task.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

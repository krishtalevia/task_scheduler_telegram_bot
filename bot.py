import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import start, add_task, auth

async def main():
    bot = Bot(token=TOKEN) 
    dp = Dispatcher()

    dp.include_routers(start.router)
    dp.include_routers(auth.router)
    dp.include_routers(add_task.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

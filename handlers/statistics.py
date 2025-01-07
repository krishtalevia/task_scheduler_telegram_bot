from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

@router.message(Command('statistics'))
async def statistics_handler(message: types.Message, command: CommandObject):
    telegram_id = message.from_user.id
    args = command.args

    if not db_manager.get_user(telegram_id):
        await message.answer('❌ Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь.')
        return
    
    if not db_manager.is_user_authorized(telegram_id):
        await message.answer('❌ Вы не авторизованы. Пожалуйста, авторизуйтесь.')
        return
    
    tasks = db_manager.get_tasks(telegram_id)

    if not args:
        pass
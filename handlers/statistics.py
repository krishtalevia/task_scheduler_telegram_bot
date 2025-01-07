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

def show_statistics(tasks, period=None):
    if not tasks:
        return '❌ Задачи не найдены.'
    
    current_time_no_ms = datetime.datetime.now().replace(microsecond=0)
    
    completed_tasks = 0
    tasks_in_progress = 0
    expired_tasks = 0

    if not period:
        for task in tasks:
            created_time = datetime.strptime(task[7], '%Y-%m-%d %H:%M:%S')
            deadline = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
            completed_time = datetime.strptime(task[8], '%Y-%m-%d %H:%M:%S')
            
            if task[6] == 1:
                completed_tasks += 1
            if task[6] == 0:
                tasks_in_progress += 1
            if task[6] == 0 and current_time_no_ms > deadline:
                expired_tasks += 1
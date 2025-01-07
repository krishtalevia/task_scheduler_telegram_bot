from datetime import datetime, timedelta

from aiogram import Router, types
from aiogram.filters import Command, CommandObject, StateFilter

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

@router.message(StateFilter(None), Command('statistics'))
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
    expired_tasks_in_progress = 0
    completed_on_time = 0
    total_tasks = 0
    total_time = timedelta()

    for task in tasks:
        created_time = datetime.strptime(task[7], '%Y-%m-%d %H:%M:%S')
        deadline = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
        completed_time = datetime.strptime(task[8], '%Y-%m-%d %H:%M:%S')
        
        if task[6] == 1:
            if period:
                start_date, end_date = period
                if start_date <= created_time <= end_date:
                    total_time += (completed_time - created_time)
                    completed_tasks += 1
                    if completed_time <= deadline:
                        completed_on_time += 1

            else:
                total_time += (completed_time - created_time)
                completed_tasks += 1
                if completed_time <= deadline:
                    completed_on_time += 1

        if task[6] == 0:
            if period:
                start_date, end_date = period
                if start_date <= created_time <= end_date:
                    tasks_in_progress += 1
                    if current_time_no_ms > deadline:
                        expired_tasks_in_progress += 1
            else:
                tasks_in_progress += 1
                if current_time_no_ms > deadline:
                    expired_tasks_in_progress += 1
        
        total_tasks += 1

    average_time = total_time / completed_tasks if completed_tasks > 0 else timedelta()
    on_time_percentage = (completed_on_time / total_tasks) * 100 if total_tasks > 0 else 0

    statistics = [
        f'✅ Завершённые задачи: {completed_tasks}',
        f'🔄 В процессе выполнения: {tasks_in_progress}',
        f'❌ Просроченные задачи: {expired_tasks_in_progress}',
        f'⏱ Среднее время завершения задачи: {average_time}',
        f'📊 Процент задач, выполненных в срок: {round(on_time_percentage, 2)}'
    ]

    return '\n'.join(statistics)
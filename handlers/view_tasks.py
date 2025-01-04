from datetime import datetime, timedelta
from aiogram import Router, types
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from handlers.auth import AuthStates
from model import DatabaseManager, Task

router = Router()
db_manager = DatabaseManager()

@router.message(StateFilter(AuthStates.authorized), Command('view_tasks'))
async def view_tasks_handler(message: types.Message, command: CommandObject, state: FSMContext):
    telegram_id = message.from_user.id
    args = command.args

    tasks = db_manager.get_tasks(telegram_id)

    if not tasks:
        await message.answer('У вас нет задач.')

    if not args:
        await message.answer(show_tasks(tasks))

    elif 'приоритет' in args:
        if '=' in args:
            priority = args.split('=')[1].strip().lower()
            filtered_tasks = filter_tasks_by_priority(tasks, priority)
    
            if filtered_tasks:
                await message.answer(show_tasks(filtered_tasks))
            else:
                await message.answer(f'Задач с приоритетом {priority} нет.')
        
        else:
            sorted_tasks = sort_tasks_by_priority(tasks)
            await message.answer(show_tasks(sorted_tasks))

    elif 'срок' in args:
        if '=' in args:
            deadline_type = args.split('=')[1].strip().lower()
            filtered_tasks = filter_tasks_by_deadline(tasks, deadline_type)
            if filtered_tasks:
                await message.answer(show_tasks(filtered_tasks))
            else:
                await message.answer(f'Задач со сроком {deadline_type} нет.')
        
        else:
            sorted_tasks = sort_tasks_by_deadline(tasks)
            await message.answer(show_tasks(sorted_tasks))
    
    elif 'период' in args:
        if '=' in args:
            dates = args.split('=').strip().split()
            if len(dates) == 2:
                start_date, end_date = dates
                filtered_tasks = filter_tasks_by_custom_period(tasks, start_date, end_date)
                if filtered_tasks:
                    await message.answer(show_tasks(filtered_tasks))
                else:
                    await message.answer('Нет задач на заданный период.')
            else:
                await message.answer('Неверный формат периода. (Пример: /view_tasks период 2025-01-01 2025-02-01)')

    elif 'статус' in args:
        if '=' in args:
            status = args.split('=').strip()
            filtered_tasks = filter_tasks_by_status(tasks, status)
            if filtered_tasks:
                await message.answer(show_tasks(filtered_tasks))
            else:
                await message.answer(f'Нет задач со статусом {status}')
        
        else:
            sorted_tasks = sort_tasks_by_status(tasks)
            await message.answer(show_tasks(sorted_tasks))

def filter_tasks_by_priority(tasks, priority):
    priority = priority.lower()
    filtered_tasks = []

    for task in tasks:
        if task['priority'].lower() == priority:
            filtered_tasks.append(task)

    return filtered_tasks

def sort_tasks_by_priority(tasks):
    priority_order = {'высокий': 1, 'средний': 2, 'низкий': 3}

    for i in range(len(tasks)):
        for j in range(0, len(tasks) - i - 1):
            priority_a = priority_order[tasks[j]['priority'].lower()]
            priority_b = priority_order[tasks[j + 1]['priority'].lower()]

            if priority_a > priority_b:
                tasks[j], tasks[j + 1] = tasks[j + 1], tasks[j]
    return tasks

def sort_tasks_by_deadline(tasks):
    for i in range(len(tasks)):
        for j in range(0, len(tasks) - i - 1):
            date_a = datetime.strptime(tasks[j]['deadline'], '%Y-%m-%d')
            date_b = datetime.strptime(tasks[j + 1]['deadline'], '%Y-%m-%d')

            if date_a > date_b:
                tasks[j], tasks[j + 1] = tasks[j + 1], tasks[j]
    
    return tasks

def sort_tasks_by_status(tasks):
    status_order = {'Выполнена': 1, 'В процессе': 2}

    for i in range(len(tasks)):
        for j in range(0, len(tasks) - i - 1):
            task_a = status_order[tasks[j]['status'].lower()]
            task_b = status_order[tasks[j + 1]['status'].lower()]

            if task_a > task_b:
                tasks[j], tasks[j + 1] = tasks[j +1], tasks[j]
    
    return tasks

def filter_tasks_by_deadline(tasks, deadline_type):
    today = datetime.today().date()
    filtered_tasks = []

    if deadline_type == 'сегодня':
        for task in tasks:
            task_deadline = datetime.strptime(task['deadline'], '%Y-%m-%d')
            if task_deadline.date() == today:
                filtered_tasks.append(task)
            
    elif deadline_type == 'неделя':
        week_ahead = today + timedelta(days=7)

        for task in tasks:
            task_deadline = datetime.strptime(task['deadline'], '%Y-%m-%d').date()
            if today <= task_deadline <= week_ahead:
                filtered_tasks.append(task)

    return filtered_tasks

def filter_tasks_by_custom_period(tasks, start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    filtered_tasks = []

    for task in tasks:
        task_deadline = datetime.trptime(task['deadline'], '%Y-%m-%d').date()
        if start_date <= task_deadline <= end_date:
            filtered_tasks.append(task)

    return filtered_tasks

def filter_tasks_by_status(tasks, status):
    filtered_tasks = []

    for task in tasks:
        if task['status'] == status:
            filtered_tasks.append(task)

    return filtered_tasks

def show_tasks(tasks):
    if not tasks:
        return '❌ Задачи не найдены.'
    
    result = []
    for task in tasks:
        title = task['title']
        description = task['description']
        deadline = task['deadline']
        priority = task['priority']

        result.append(
            f"📌 {title}\n"
            f"📖 {description}\n"
            f"📅 {deadline}\n"
            f"🎯 {priority}\n"
        )

    return '\n'.join(result)
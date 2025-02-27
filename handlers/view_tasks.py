from datetime import datetime, timedelta
from aiogram import Router, types
from aiogram.filters import Command, CommandObject, StateFilter

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

@router.message(StateFilter(None), Command('view_tasks'))
async def view_tasks_handler(message: types.Message, command: CommandObject):
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
                await message.answer(f'Задач со сроком на {deadline_type} нет.')
        
        else:
            sorted_tasks = sort_tasks_by_deadline(tasks)
            await message.answer(show_tasks(sorted_tasks))
    
    elif 'период' in args:
        if '=' in args:
            dates = args.split('=')[1].split()
            if len(dates) == 2:
                start_date, end_date = dates
                filtered_tasks = filter_tasks_by_custom_period(tasks, start_date, end_date)
                if filtered_tasks:
                    await message.answer(show_tasks(filtered_tasks))
                else:
                    await message.answer('Нет задач на заданный период.')
            else:
                await message.answer('Неверный формат периода. (Пример: /view_tasks период=2025-01-01 2025-02-01)')

    elif 'статус' in args:
        if '=' in args:
            status = args.split('=')[1].strip()
            filtered_tasks = filter_tasks_by_status(tasks, status)
            if filtered_tasks:
                await message.answer(show_tasks(filtered_tasks))
            else:
                await message.answer(f'Нет задач со статусом {status}')
        
        else:
            sorted_tasks = sort_tasks_by_status(tasks)
            await message.answer(show_tasks(sorted_tasks))
    
    elif 'поиск' in args:
        if '=' in args:
            keyword = args.split('=')[1].strip()
            filtered_tasks = db_manager.get_tasks_by_keyword(telegram_id, keyword)
            if filtered_tasks:
                await message.answer(show_tasks(filtered_tasks))
            else:
                await message.answer(f'Нет задач содержащих слово "{keyword}".')
        else:
            await message.answer('Некорректный ввод. (Пример /view_tasks поиск=купить)')

def sort_tasks_by_priority(tasks):
    priority_order = {'высокий': 1, 'средний': 2, 'низкий': 3}

    for i in range(len(tasks)):
        for j in range(0, len(tasks) - i - 1):
            priority_a = priority_order[tasks[j][5].lower()]
            priority_b = priority_order[tasks[j + 1][5].lower()]

            if priority_a > priority_b:
                tasks[j], tasks[j + 1] = tasks[j + 1], tasks[j]
    return tasks

def sort_tasks_by_deadline(tasks):
    for i in range(len(tasks)):
        for j in range(0, len(tasks) - i - 1):
            date_a = datetime.strptime(tasks[j][4], '%Y-%m-%d %H:%M:%S')
            date_b = datetime.strptime(tasks[j + 1][4], '%Y-%m-%d %H:%M:%S')

            if date_a > date_b:
                tasks[j], tasks[j + 1] = tasks[j + 1], tasks[j]
    
    return tasks

def sort_tasks_by_status(tasks):
    for i in range(len(tasks)):
        for j in range(0, len(tasks) - i - 1):
            if tasks[j][6] > tasks[j + 1][6]:
                tasks[j], tasks[j + 1] = tasks[j +1], tasks[j]
    
    return tasks

def filter_tasks_by_priority(tasks, priority):
    priority = priority.lower()
    filtered_tasks = []

    for task in tasks:
        if task[5].lower() == priority:
            filtered_tasks.append(task)

    return filtered_tasks

def filter_tasks_by_deadline(tasks, deadline_type):
    today = datetime.today().date()
    filtered_tasks = []

    if deadline_type == 'сегодня':
        for task in tasks:
            try: 
                task_deadline = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S.%f').date()
            except ValueError:
                task_deadline = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S').date()
            if task_deadline == today:
                filtered_tasks.append(task)
            
    elif deadline_type == 'неделя':
        week_ahead = today + timedelta(days=7)

        for task in tasks:
            try: 
                task_deadline = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S.%f').date()
            except ValueError:
                task_deadline = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S').date()
            if today <= task_deadline <= week_ahead:
                filtered_tasks.append(task)

    return filtered_tasks

def filter_tasks_by_custom_period(tasks, start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    filtered_tasks = []

    for task in tasks:
        task_deadline = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S').date()
        if start_date <= task_deadline <= end_date:
            filtered_tasks.append(task)

    return filtered_tasks

def filter_tasks_by_status(tasks, status):
    status_dict = {
        'выполнена': 1,
        'не выполнена': 0, 
    }
    
    status = status_dict.get(status.lower())
    filtered_tasks = []

    for task in tasks:
        if task[6] == status:
            filtered_tasks.append(task)

    return filtered_tasks

def show_tasks(tasks):
    if not tasks:
        return '❌ Задачи не найдены.'
    
    result = []
    for task in tasks:
        task_id = task[0]
        title = task[2]
        description = task[3]
        deadline = task[4]
        priority = task[5]
        status = task[6]

        result.append(
            f'🆔 ID: {task_id}\n'
            f'📌 Название: {title}\n'
            f'📖 Описание: {description if description else "нет"}\n'
            f'📅 Срок: {deadline}\n'
            f'🎯 Приоритет: {priority}\n'
            f'{'✅' if status == 1 else '❌'} Статус: {'Выполнена' if status == 1 else 'Не выполнена'}\n'
            f'{"-" * 30}'
        )

    return '\n'.join(result)
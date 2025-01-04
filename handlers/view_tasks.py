import datetime
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

    if not args:
        await message.answer(show_tasks(tasks))

    elif 'приоритет' in args:
        if '=' in args:
            priority = args.split('=')[1].strip().lower()
            
            filtered_tasks = []
            for task in tasks:
                if task['priority'].lower() == priority:
                    filtered_tasks.append(task)
            if filtered_tasks:
                await message.answer(show_tasks(filtered_tasks))
            else:
                await message.answer(f'Задач с приоритетом {priority} нет.')
        
        else:
            priority_order = {'высокий': 1, 'средний': 2, 'низкий': 3}

            for i in range(len(tasks)):
                for j in range(0, len(tasks) - i - 1):
                    priority_a = priority_order[tasks[j]['priority'].lower()]
                    priority_b = priority_order[tasks[j + 1]['priority'].lower()]

                    if priority_a > priority_b:
                        task[j], tasks[j + 1] = tasks[j + 1], tasks[j]
            await message.answer(show_tasks(tasks))

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
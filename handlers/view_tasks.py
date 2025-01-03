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
async def view_tasks_handler(message: types.Message, state: FSMContext):
    pass

def show_tasks(tasks):
    if not tasks:
        return 'Задачи не найдены.'
    
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
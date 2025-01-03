import datetime
from aiogram import Router, types
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from handlers.auth import AuthStates
from model import DatabaseManager, Task

router = Router()
db_manager = DatabaseManager()

class AddingTaskStates(StatesGroup):
    AddingTitle = State()
    AddingDescription = State()
    AddingDeadline = State()
    AddingPriority = State()
    TaskConfirmation = State()

@router.message(StateFilter(AuthStates.authorized), Command('add_task'))
async def add_task_handler(message: types.Message, state: FSMContext):
    await state.set_state(AddingTaskStates.AddingTitle)

@router.message(StateFilter(AddingTaskStates.AddingTitle))
async def adding_title_handler(message: types.Message, state: FSMContext):
    await message.answer('Введите название задачи:')
    title = message.text
    await state.update_data(title=title)
    await state.set_state(AddingTaskStates.AddingDescription)

@router.message(StateFilter(AddingTaskStates.AddingDescription))
async def adding_description_handler(message: types.Message, state: FSMContext):
    await message.answer('Введите описание задачи (опционально):')
    description = message.text if len(message.text) > 0 else None
    await state.update_data(description=description)
    await state.set_state(AddingTaskStates.AddingDeadline)

@router.message(StateFilter(AddingTaskStates.AddingDeadline))
async def adding_deadline_handler(message: types.Message, state: FSMContext):
    while True:
        await message.answer('Введите дату исполнения задачи (ГГГГ-ММ-ДД): ')
        date = message.text
    
        try:
            deadline = datetime.strptime(date, '%Y-%m-%d')
            await state.update_data(deadline=deadline)
            break
        except ValueError:
            await message.answer('Неверный формат. Введите дату в формате ГГГГ-ММ-ДД.')
        
    await state.set_state(AddingTaskStates.AddingPriority)

@router.message(StateFilter(AddingTaskStates.AddingPriority))
async def adding_priority_handler(message: types.Message, state: FSMContext):
    while True:
        await message.answer('Введите приоритет задачи (низкий, средний, высокий):')
        priority = message.text

    
        if priority in ('низкий', 'средний', 'высокий'):
            await state.update_data(priority=priority)
            break
        else:
            await message.answer('Приоритет задачи может иметь одно из следующих значений: "низкий", "средний" или "высокий".')
    
    await state.set_state(AddingTaskStates.TaskConfirmation)

@router.message(StateFilter(AddingTaskStates.TaskConfirmation))
async def task_adding_confirmation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    title = data['title']
    description = data['description']
    deadline = data['deadline']
    priority = data['priority']
    
    await message.answer(
        f'📝 Задача:\n'
        f'📌 Название: {title}\n'
        f'📖 Описание: {description if description else "нет"}\n'
        f'📅 Срок: {deadline}\n'
        f'🎯 Приоритет: {priority}\n\n'
        f'Добавить данную задачу (Да/Нет)?'
    )

    while True:
        if message.text.lower() == 'да':
            telegram_id = message.from_user.id
            task = Task(telegram_id, title, description, deadline, priority)
            

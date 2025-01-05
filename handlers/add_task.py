import datetime
from aiogram import Router, types
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from model import DatabaseManager, Task

router = Router()
db_manager = DatabaseManager()

class AddingTaskStates(StatesGroup):
    AddingTitle = State()
    AddingDescription = State()
    AddingDeadline = State()
    AddingPriority = State()
    TaskReview = State()
    TaskAddingConfirmation = State()

@router.message(Command('add_task'))
async def add_task_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id

    user = db_manager.get_tasks(telegram_id)
    if not user:
        await message.answer('❌ Вы не зарегистрированы. Используйте команду /register для регистрации.')
        return
    
    if not db_manager.is_user_authorized(telegram_id):
        await message.answer('❌ Вы не авторизованы. Используйте команду /login для авторизации.')
        return
    
    await state.set_state(AddingTaskStates.AddingTitle)

@router.message(StateFilter(AddingTaskStates.AddingTitle))
async def adding_title_handler(message: types.Message, state: FSMContext):
    await message.answer('Введите название задачи:')
    
    if not message.text.strip():
        await message.answer('⚠️ Пустой ввод. Повторите попытку.')
        return

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
    date = message.text.strip()

    try:
        deadline = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        await state.update_data(deadline=deadline)

        await state.set_state(AddingTaskStates.AddingPriority)
    except ValueError:
        await message.answer('⚠️ Неверный формат. Введите дату в формате ГГГГ-ММ-ДД.')

@router.message(StateFilter(AddingTaskStates.AddingPriority))
async def adding_priority_handler(message: types.Message, state: FSMContext):
    await message.answer('Введите приоритет задачи (низкий, средний, высокий):')
    priority = message.text
    
    if priority in ('низкий', 'средний', 'высокий'):
        await state.update_data(priority=priority)
        await state.set_state(AddingTaskStates.TaskReview)
    else:
        await message.answer('Приоритет задачи может иметь одно из следующих значений: "низкий", "средний" или "высокий".')

@router.message(StateFilter(AddingTaskStates.TaskReview))
async def task_review(message: types.Message, state: FSMContext):
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

    await state.set_state(AddingTaskStates.TaskAddingConfirmation)

@router.message(StateFilter(AddingTaskStates.TaskAddingConfirmation))
async def task_adding_confirmation(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        telegram_id = message.from_user.id
        data = await state.get_data()
        title = data['title']
        description = data['description']
        deadline = data['deadline']
        priority = data['priority']

        task = Task(telegram_id, title, description, deadline, priority)
        try:
            db_manager.add_task(task)
            await message.answer('✅ Задача успешно добавлена!')
            await state.clear()
            await state.set_state(AuthStates.authorized)
        except Exception:
            await message.answer('⚠️ Произошла ошибка при добавлении задачи. Попробуйте снова.')

    elif message.text.lower() == 'нет':
        await message.answer('❌ Добавление задачи отменено.')
        await state.clear()
        await state.set_state(AuthStates.authorized)

    else:
        await message.answer('⚠️ Ответ должен содержать одно из значений: "Да" или "Нет".')
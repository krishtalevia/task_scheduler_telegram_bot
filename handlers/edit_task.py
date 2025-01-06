from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import StatesGroup, State

from model import DatabaseManager

class EditTaskStates(StatesGroup):
    ChoosingParameter = State()
    EditingParameter = State()

router = Router()
db_manager = DatabaseManager()

@router.message(Command('edit_task'))
async def edit_task_handler(message: types.Message, state: FSMContext):
    await message.answer('Введите ID задачи, которую хотите изменить:')
    await state.set_state(EditTaskStates.ChoosingParameter)

@router.message(StateFilter(EditTaskStates.ChoosingParameter))
async def choosing_parameter_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    task_id = message.text.strip()

    task = db_manager.get_task_by_id(telegram_id, task_id)

    if not task:
        await message.answer('❌ Задача с таким ID не найдена.')
        await state.clear()
        return
    
    await state.update_data(task_id=task_id)
    await message.answer(
        "Какой параметр задачи вы хотите изменить?\n"
        "1. Название\n"
        "2. Описание\n"
        "3. Срок\n"
        "4. Приоритет\n\n"
        "Введите номер или название параметра:"
    )
    await state.set_state(EditTaskStates.EditingParameter)

@router.message(StateFilter(EditTaskStates.EditingParameter))
async def editing_parameter_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    input_parameter = message.text.strip().lower()

    parameters = {
        '1': 'title',
        '2': 'description',
        '3': 'deadline',
        '4': 'priority',
    }

    if input_parameter not in parameters:
        await message.answer('⚠️ Некорректный выбор параметра. Попробуйте снова.')
        return
    
    chosen_parameter = parameters[input_parameter]
    await state.update_data(chosen_parameter=chosen_parameter)
    
    parameter_edit_text = {
        'title': 'Введите новое название задачи:',
        'description': 'Введите новое описание задачи:',
        'deadline': 'Введите новый срок задачи в формате ГГГГ-ММ-ДД ЧЧ:ММ',
        'priority': 'Введите новый приоритет задачи (низкий, средний, высокий):',
    }[chosen_parameter]

    await message.answer(parameter_edit_text)
    await state.set_state(EditTaskStates.ChoosingParameter)
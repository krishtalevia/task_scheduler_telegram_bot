from aiogram import Router, types
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from handlers.auth import AuthStates

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

class AddingTaskStates(StatesGroup):
    AddingTitle = State()
    AddingDescription = State()
    AddingDeadline = State()
    AddingPriority = State()

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
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import StatesGroup, State

from model import DatabaseManager

class EditTaskStates(StatesGroup):
    ChoosingParameter = State()
    EditinParameter = State()

router = Router()
db_manager = DatabaseManager()

@router.message(Command('edit_task'))
async def edit_task_handler(message: types.Message, state: FSMContext):
    await message.answer('Введите ID задачи, которую хотите изменить:')
    await state.set_state(EditTaskStates.ChoosingParameter)
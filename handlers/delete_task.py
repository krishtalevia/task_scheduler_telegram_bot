from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import StatesGroup, State

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

class DeleteTaskStates(StatesGroup):
    Deleting = State()

@router.message(StateFilter(None), Command('delete_task'))
async def delete_task_handler(message: types.Message, state: FSMContext):
    await message.answer('Введите ID задачи, которую требуется удалить:')
    await state.set_state(DeleteTaskStates.Completing)
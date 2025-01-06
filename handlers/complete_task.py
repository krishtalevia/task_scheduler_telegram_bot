from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import StatesGroup, State

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

class CompleteTaskStates(StatesGroup):
    WaitingForTaskId = State()
    CheckingTaskExistence = State()

@router.message(StateFilter(None), Command('complete_task'))
async def complete_task_handler(message: types.Message, state: FSMContext):
    await message.answer('Введите ID задачи, которую требуется пометить как выполненную:')
    await state.set_state(CompleteTaskStates.WaitingForTaskId)
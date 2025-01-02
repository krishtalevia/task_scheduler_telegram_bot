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
    pass
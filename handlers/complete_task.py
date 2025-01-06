from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import StatesGroup, State

from model import DatabaseManager


router = Router()
db_manager = DatabaseManager()

@router.message(StateFilter(None), Command('complete_task'))
async def complete_task_handler(message: types.Message, state: FSMContext):
    pass
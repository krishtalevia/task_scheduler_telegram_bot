from aiogram import Router, types
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

class AuthStates(StatesGroup):
    registered = State()

@router.message(StateFilter(None), Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    if db_manager.get_user(telegram_id) is None:
        await message.answer('Для начала работы с ботом зарегистрируйтесь командой "/register"')
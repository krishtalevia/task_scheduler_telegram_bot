from aiogram import Router, types
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

class AuthStates(StatesGroup):
    authorized = State()

@router.message(StateFilter(None), Command('register'))
async def register_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    if db_manager.get_user(telegram_id) is None:
        db_manager.register_user
        await message.answer('Вы успешно зарегистрировались. Для авторизации используйте /login')
    else:
        await message.answer('Вы уже зарегистрированы.')
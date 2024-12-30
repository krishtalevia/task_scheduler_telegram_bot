from aiogram import Router, types
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

class AuthStates(StatesGroup):
    waiting_for_username = State()
    registered = State()

@router.message(StateFilter(None), Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    if db_manager.get_user(telegram_id) is not None:
        await state.set_state(AuthStates.registered)
        await message.answer('Добро пожаловать. Снова.')
        # Вывод вариантов команд
    else:
        await state.set_state(AuthStates.waiting_for_username)
        await message.answer('Введите имя пользователя для регистрации:')

@router.message(StateFilter(AuthStates.waiting_for_username))
async def submit_username(message: types.Message, state: FSMContext):
    username = message.text
    telegram_id = message.from_user.id
    if db_manager.register_user(telegram_id, username):
        await message.answer('Вы успешно зарегистрировались.')
        await state.set_state(AuthStates.registered)
    else:
        await message.answer('Произошла ошибка при попытке регистрации. Попробуйте снова')
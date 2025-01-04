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
        if db_manager.register_user(telegram_id):
            await message.answer('Вы успешно зарегистрировались. Для авторизации используйте /login')
        else:
           await message.answer('Во время регистрации произошла ошибка.')
    else:
        await message.answer('Вы уже зарегистрированы. Используйте /login для авторизации')

@router.message(StateFilter(None), Command('login'))
async def login_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    current_state = await state.get_state()
    if db_manager.get_user(telegram_id) is None:
        await message.answer('Пользователь не найден. Для регистрации используйте /register')
    elif current_state == AuthStates.authorized.state:
        await message.answer('Вы уже авторизованы.')
    else:
        await state.set_state(AuthStates.authorized)
        await message.answer('Вы успешно авторизованы.')
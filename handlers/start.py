from aiogram import Router, types
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from handlers.auth import AuthStates

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

@router.message(StateFilter(None), Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user = db_manager.get_user(telegram_id)
    current_state = await state.get_state()

    registration_status = "✅ Зарегистрирован" if user else "❌ Не зарегистрирован"
    authorization_status = "✅ Авторизован" if current_state == AuthStates.authorized.state else "❌ Не авторизован"

    await message.answer(
        f'👋 Данный бот предназначен для управления личными задачами.\n\n'
        f'📋 Этот бот позволяет:\n'
        f'• Управлять задачами\n'
        f'• Устанавливать дедлайны и приоритеты\n'
        f'• Получать напоминания о приближении сроков\n\n'
        f'🔒 Для работы требуется регистрация и авторизация.\n\n'
        f'Ваш статус:\n'
        f'{registration_status}\n'
        f'{authorization_status}\n\n'
        f'ℹ️ Для регистрации используйте команду /register.\n'
        f'Для авторизации — /login.\n'
        f'Список доступных команд — /help.'
    )
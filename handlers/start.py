from aiogram import Router, types
from aiogram.filters import Command

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

@router.message(Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    
    user = db_manager.get_user(telegram_id)
    if not user:
        registration_status = "❌ Не зарегистрирован"
        authorization_status = "❌ Не авторизован"
    else:
        registration_status = "✅ Зарегистрирован"
        if db_manager.is_user_authorized(telegram_id):
            authorization_status = "✅ Авторизован"
        else:
            authorization_status = "❌ Не авторизован"

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
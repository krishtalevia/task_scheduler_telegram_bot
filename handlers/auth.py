from aiogram import Router, types
from aiogram.filters import Command, StateFilter


from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

@router.message(StateFilter(None), Command('register'))
async def register_handler(message: types.Message):    
    telegram_id = message.from_user.id
    if db_manager.get_user(telegram_id) is None:
        if db_manager.register_user(telegram_id):
            await message.answer('✅ Вы успешно зарегистрировались. Для авторизации используйте /login')
        else:
           await message.answer('❌ Во время регистрации произошла ошибка.')
    else:
        await message.answer('⚠️ Вы уже зарегистрированы. Используйте /login для авторизации')

@router.message(StateFilter(None), Command('login'))
async def login_handler(message: types.Message):
    telegram_id = message.from_user.id

    user = db_manager.get_user(telegram_id)
    if user is None:
        await message.answer('❌ Пользователь не найден. Для регистрации используйте /register')
    elif db_manager.is_user_authorized(telegram_id):
        await message.answer('⚠️ Вы уже авторизованы.')
    else:
        db_manager.authorize_user(telegram_id)
        await message.answer('✅ Вы успешно авторизованы.')
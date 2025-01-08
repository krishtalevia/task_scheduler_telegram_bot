import pytest
from aiogram import types
from aiogram.types import Message

from model import DatabaseManager, init_db
from handlers import auth

@pytest.fixture
def db_manager():
    db_manager = DatabaseManager()
    init_db()
    return db_manager

# Тестовый случай 1.1: Попытка регистрации уже зарегистрированного пользователя
def test_register_existing_user(db_manager):
    telegram_id = 1
    db_manager.register_user(telegram_id)

    with pytest.raises(ValueError, match='Пользователь уже существует!'):
        db_manager.register_user(telegram_id)
        db_manager.delete_user(telegram_id)

# Тестовый случай 1.2: Успешная регистрация нового пользователя
def test_register_new_user(db_manager):
    telegram_id = 2
    
    result = db_manager.register_user(telegram_id)
    assert result is True
    assert db_manager.get_user(telegram_id) is not None
    db_manager.delete_user(telegram_id)


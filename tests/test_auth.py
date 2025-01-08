import pytest

from model import DatabaseManager, init_db

@pytest.fixture
def db_manager():
    db_manager = DatabaseManager()
    init_db()
    db_manager.delete_all_users()

    yield db_manager
    
    db_manager.close()

# Тестовый случай 1.1: Попытка регистрации уже зарегистрированного пользователя
def test_register_existing_user(db_manager):
    telegram_id = 1
    db_manager.register_user(telegram_id)

    with pytest.raises(ValueError, match='Пользователь уже существует!'):
        db_manager.register_user(telegram_id)

# Тестовый случай 1.2: Успешная регистрация нового пользователя
def test_register_new_user(db_manager):
    telegram_id = 2
    
    result = db_manager.register_user(telegram_id)
    assert result is True
    assert db_manager.get_user(telegram_id) is not None

# Тестовый случай 1.3: Авторизация зарегистрированного пользователя
def auth_registered_user(db_manager):
    telegram_id = 3
    db_manager.register_user(telegram_id)

    result = db_manager.authorize_user(telegram_id)
    assert result is True

    assert db_manager.is_user_authorized(telegram_id) is True

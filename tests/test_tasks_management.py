import pytest
import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext
from handlers.add_task import add_task_handler, adding_title_handler, adding_description_handler, adding_deadline_handler, adding_priority_handler, task_adding_confirmation
from model import DatabaseManager, init_db

from model import DatabaseManager, init_db

@pytest.fixture
def db_manager():
    db_manager = DatabaseManager()
    init_db()
    yield db_manager
    db_manager.close()

@pytest.fixture
def fsm_context():
    return FSMContext()

@pytest.fixture
def message():
    return types.Message()

@pytest.fixture
def register_user(db_manager):
    telegram_id = 123
    db_manager.register_user(telegram_id)
    return telegram_id

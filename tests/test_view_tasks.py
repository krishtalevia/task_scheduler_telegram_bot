import pytest
import datetime
from model import DatabaseManager, init_db
from handlers.view_tasks import (
    filter_tasks_by_priority,
    filter_tasks_by_deadline,
    filter_tasks_by_custom_period,
    filter_tasks_by_status,
    sort_tasks_by_deadline,
    sort_tasks_by_priority,
    sort_tasks_by_status,
    show_tasks
)

@pytest.fixture(scope='module')
def test_db():
    init_db()
    db_manager = DatabaseManager('database.db')
    yield db_manager
    db_manager.delete_all_users()
    db_manager.close()

@pytest.fixture(scope='module')
def test_user(test_db):
    telegram_id = 1
    test_db.register_user(telegram_id)
    test_db.authorize_user(telegram_id)
    yield telegram_id
    test_db.delete_user(telegram_id)

def test_view_tasks_for_today(test_db, test_user):
    telegram_id = test_user
    title = 'Тестовая задача на сегодня'
    description = 'Тестовое описание'
    deadline = datetime.datetime.now().replace(microsecond=0)
    priority = 'Высокий'
    created_at = datetime.datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')

    test_db.add_task(telegram_id, title, description, deadline, priority, created_at)

    tasks = test_db.get_tasks(telegram_id)
    filtered_tasks = filter_tasks_by_deadline(tasks, 'сегодня')

    assert filtered_tasks is not None

def test_filter_tasks_by_priority(test_db, test_user):
    telegram_id = test_user
    title = 'Тестовая задача на сегодня'
    description = 'Тестовое описание'
    deadline = datetime.datetime.now().replace(microsecond=0)
    created_at = datetime.datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')

    test_db.add_task(telegram_id, title, description, deadline, 'Низкий', created_at)
    test_db.add_task(telegram_id, title, description, deadline, 'Средний', created_at)
    test_db.add_task(telegram_id, title, description, deadline, 'Высокий', created_at)

    tasks = test_db.get_tasks(telegram_id)
    filtered_tasks = filter_tasks_by_priority(tasks, 'Высокий')

    assert filtered_tasks is not None

def test_filter_tasks_by_keyword(test_db, test_user):
    telegram_id = test_user
    title = 'Тестовая задача с ключевым словом'
    description = 'Тестовое описание'
    deadline = datetime.datetime.now().replace(microsecond=0)
    priority = 'Низкий'
    created_at = datetime.datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')

    test_db.add_task(telegram_id, title, description, deadline, priority, created_at)

    tasks = test_db.get_tasks_by_keyword(telegram_id, 'словом')

    assert tasks is not None
import pytest
import datetime
from model import DatabaseManager, init_db

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

def test_add_task(test_db, test_user):
    telegram_id = test_user
    title = 'Тестовая задача'
    description = 'Тестовое описание'
    deadline = datetime.datetime.now() + datetime.timedelta(hours=1)
    priority = 'Высокий'
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    test_db.add_task(telegram_id, title, description, deadline, priority, created_at)

    tasks = test_db.get_tasks(telegram_id)

    assert tasks is not None
    task = tasks[0]
    assert task[2] == title

def test_edit_task_deadline(test_db, test_user):
    telegram_id = test_user
    title = 'Тестовая задача'
    description = 'Тестовое описание'
    deadline = datetime.datetime.now() + datetime.timedelta(hours=1)
    priority = 'Высокий'
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_deadline = datetime.datetime.strptime('2025-01-10 18:00:00', '%Y-%m-%d %H:%M:%S')

    test_db.add_task(telegram_id, title, description, deadline, priority, created_at)

    test_db.update_task(telegram_id, 1, 'deadline', new_deadline)

    task = test_db.get_task_by_id(telegram_id, 1)
    assert task[4] == '2025-01-10 18:00:00'
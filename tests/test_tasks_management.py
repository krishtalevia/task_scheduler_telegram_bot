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
    tasks = test_db.get_tasks(telegram_id)
    task_id = tasks[0][0]

    test_db.update_task(telegram_id, task_id, 'deadline', new_deadline)

    tasks = test_db.get_tasks(telegram_id)
    assert tasks[0][4] == '2025-01-10 18:00:00'

def test_edit_task_priority(test_db, test_user):
    telegram_id = test_user
    title = 'Тестовая задача'
    description = 'Тестовое описание'
    deadline = datetime.datetime.now() + datetime.timedelta(hours=1)
    priority = 'Высокий'
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_priority = 'Средний'

    test_db.add_task(telegram_id, title, description, deadline, priority, created_at)

    tasks = test_db.get_tasks(telegram_id)
    task_id = tasks[0][0]
    test_db.update_task(telegram_id, task_id, 'priority', new_priority)

    tasks = test_db.get_tasks(telegram_id)
    assert tasks[0][5] == new_priority

def test_delete_task(test_db, test_user):
    telegram_id = test_user
    title = 'Тестовая задача'
    description = 'Тестовое описание'
    deadline = datetime.datetime.now() + datetime.timedelta(hours=1)
    priority = 'Высокий'
    created_at = datetime.datetime.now()

    test_db.add_task(telegram_id, title, description, deadline, priority, created_at)

    tasks = test_db.get_tasks(telegram_id)
    assert tasks[0] is not None
    
    task_id = tasks[0][0]
    test_db.delete_task(telegram_id, task_id)

    task = test_db.get_task_by_id(telegram_id, task_id)
    assert task is None

def test_complete_task(test_db, test_user):
    telegram_id = test_user
    title = 'Тестовая задача'
    description = 'Тестовое описание'
    deadline = datetime.datetime.now() + datetime.timedelta(hours=1)
    priority = 'Высокий'
    created_at = datetime.datetime.now()

    test_db.add_task(telegram_id, title, description, deadline, priority, created_at)
    tasks = test_db.get_tasks(telegram_id)

    assert tasks[0][6] == 0

    task_id = tasks[0][0]
    test_db.update_task(telegram_id, task_id, 'status', True)
    task = test_db.get_task_by_id(telegram_id, task_id)
    assert task[6] == 1
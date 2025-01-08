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
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
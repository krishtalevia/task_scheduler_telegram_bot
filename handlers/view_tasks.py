import datetime
from aiogram import Router, types
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from handlers.auth import AuthStates
from model import DatabaseManager, Task

router = Router()
db_manager = DatabaseManager()
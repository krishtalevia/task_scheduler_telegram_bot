from aiogram import Router, F, types
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from model import DatabaseManager

class AuthStates(StatesGroup):
    registration_check = State()
    waiting_for_username = State()
    registered = State()
from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()
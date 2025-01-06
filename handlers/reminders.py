import datetime

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import StatesGroup, State

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

class ReminderStates(StatesGroup):
    ChooseReminderTime = State()

@router.message(StateFilter(None), Command('reminders'))
async def reminders_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "Выберите время напоминания, напшите номер или текст:\n"
        "1️⃣ За 1 час\n"
        "2️⃣ За 2 часа\n"
        "3️⃣ За 1 день\n"
    )
    await state.set_state(ReminderStates.ChooseReminderTime)

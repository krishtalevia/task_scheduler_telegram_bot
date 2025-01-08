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
        "4️⃣ Отключить"
    )
    
    await state.set_state(ReminderStates.ChooseReminderTime)

@router.message(StateFilter(ReminderStates.ChooseReminderTime))
async def reminder_choice_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user_choice = message.text.lower()

    if user_choice in ['1', 'за 1 час', '1 час']:
        await message.answer('⏳ Вы выбрали напоминание за 1 час.')
        db_manager.set_user_reminder_time(telegram_id, 1)
    elif user_choice in ['2', 'за 2 часа', '2 часа']:
        await message.answer('⏳ Вы выбрали напоминание за 2 часа.')
        db_manager.set_user_reminder_time(telegram_id, 2)
    elif user_choice in ['3', 'за 1 день', '1 день']:
        await message.answer('⏳ Вы выбрали напоминание за 1 день.')
        db_manager.set_user_reminder_time(telegram_id, 24)
    elif user_choice in ['4', 'Отключить', 'отключить']:
        await message.answer('⏳ Вы выбрали отключение напоминаний.')
        db_manager.set_user_reminder_time(telegram_id, 0)
    else:
        await message.answer('⚠️ Неверный ввод.')
        await state.clear()
        return
    
    await state.clear()
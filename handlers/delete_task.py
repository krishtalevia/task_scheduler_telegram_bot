from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import StatesGroup, State

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

class DeleteTaskStates(StatesGroup):
    Deleting = State()

@router.message(StateFilter(None), Command('delete_task'))
async def delete_task_handler(message: types.Message, state: FSMContext):
    await message.answer('🆔 Введите ID задачи, которую требуется удалить:')
    await state.set_state(DeleteTaskStates.Deleting)

@router.message(StateFilter(DeleteTaskStates.Deleting))
async def deleting_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    task_id = message.text
    task = db_manager.get_task_by_id(telegram_id, task_id)

    if task:
        if db_manager.delete_task(telegram_id, task_id):
            await message.answer('✅ Задача удалена.')
        else:
            await message.answer('⚠️ В процессе удаления задачи произошла ошибка.')
    else:
        await message.answer('⚠️ Задачи с таким ID нет.')

    state.clear()
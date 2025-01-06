from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import StatesGroup, State

from model import DatabaseManager

router = Router()
db_manager = DatabaseManager()

class CompleteTaskStates(StatesGroup):
    Completing = State()

@router.message(StateFilter(None), Command('complete_task'))
async def complete_task_handler(message: types.Message, state: FSMContext):
    await message.answer('Введите ID задачи, которую требуется пометить как выполненную:')
    await state.set_state(CompleteTaskStates.Completing)

@router.message(StateFilter(CompleteTaskStates.Completing))
async def completing_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    task_id = message.text
    task = db_manager.get_task_by_id(telegram_id, task_id)

    if task:
        if task[6] == 1:
            await message.answer(f'⚠️ Задача с ID {task_id} уже выполнена.')

        elif task[6] == 0:
            if db_manager.update_task(telegram_id, task_id, parameter_name='status', new_value=True):
                await message.answer(f'🎉 Задача с ID {task_id} теперь выполнена.')
            else:
                await message.answer('⚠️ При выполнении операции произошла ошибка.')
    else:
        await message.answer(f'⚠️ Задача с ID {task_id} не найдена.')
    
    await state.clear()
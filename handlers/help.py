from aiogram import Router, types
from aiogram.filters import Command, CommandObject

router = Router()

@router.message(Command('help'))
async def help_handler(message: types.Message, command: CommandObject):
    args = command.args

    if not args:
        await message.answer(
            f'📋 Список доступных команд:\n\n'
            f'/start – краткая инструкция по использованию бота.\n'
            f'/register – регистрация пользователя.\n'
            f'/login – авторизация пользователя.\n'
            f'/add_task – создание новой задачи.\n'
            f'/edit_task – редактирование существующей задачи.\n'
            f'/complete_task – отметка задачи как выполненной.\n'
            f'/delete_task – удаление задачи.\n'
            f'/reminders - настройка напоминаний.\n'
            f'/view_tasks [фильтр/сортировка] – просмотр списка задач. Для подробностей используйте "/help view_tasks".\n'
            f'/statistics [период] - просмотр статистики. Для подробностей используйте "/help statistics"\n'
        )
    elif args == 'view_tasks':
        await message.answer(
            f'📂 Команда /view_tasks:\n\n'
            f'Позволяет просматривать задачи с фильтрацией и сортировкой. Примеры использования:\n\n'
            f'🔹 Без фильтров:\n'
            f'/view_tasks – все задачи.\n\n'
            f'🔹 Фильтрация по приоритету:\n'
            f'/view_tasks приоритет – задачи отсортированные по убыванию приоритета.\n'
            f'/view_tasks приоритет=высокий – задачи с приоритетом "высокий" (средний и низкий приоритет вызываются по аналогии).\n\n'
            f'🔹 Фильтрация по сроку выполнения:\n'
            f'/view_tasks срок – задачи отсортированные по сроку выполнения.\n'
            f'/view_tasks срок=день – задачи с выполнением на текущий день.\n'
            f'/view_tasks срок=неделя –  задачи на текущую неделю.\n'
            f'/view_tasks период=дата_1 дата_2 – задачи в заданном периоде.\n\n'
            f'🔹 Фильтрация по статусу:\n'
            f'/view_tasks статус – задачи отсортированные по статусу.\n'
            f'/view_tasks статус=выполнена – выполненные задачи.\n'
            f'/view_tasks статус=не выполнена – невыполненные задачи.'
        )
    elif args == 'statistics':
        await message.answer(
            f'📊 Команда /statistics – просмотр статистики:\n\n'
            f'Позволяет просматривать статистику выполнения задач за определённый период. Примеры использования:\n\n'
            f'🔹 Общая статистика:\n'
            f'/statistics – статистика за весь период.\n\n'
            f'🔹 Статистика за указанный период:\n'
            f'/statistics день – статистика за день.\n'
            f'/statistics неделя – статистика за неделю.\n'
            f'/statistics месяц – статистика за месяц.\n'
        )
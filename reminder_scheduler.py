import sqlite3
import asyncio
import datetime

from model import DatabaseManager

db_manager = DatabaseManager()

async def reminder_schedule(dp):
    while True:
        try: 
            current_time = datetime.datetime.now()

            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            cursor.execute('''
                SELECT tasks.title, tasks.deadline, users.telegram_id, users.reminder_time
                FROM tasks
                JOIN users ON tasks.user_id = users.id
                WHERE tasks.status = 0
            ''')
            tasks_to_remind = cursor.fetchall()
            connection.close()

            for title, deadline, telegram_id, reminder_time in tasks_to_remind:
                reminder_time_delta = datetime.timedelta(hours=reminder_time)
                reminder_time_point = deadline - reminder_time_delta

                if reminder_time_point <= current_time < deadline:
                    minutes_left = (deadline - current_time).seconds // 60
                    await dp.send_message(
                        chat_id=telegram_id,
                        text=f'⏳ Напоминание! До задачи "{title}" осталось {minutes_left} минут.'
                        )
                
            await asyncio.sleep(60)
        
        except Exception:
            print('Произошла ошибка в планировщике напоминаний.')
            await asyncio.sleep(60)

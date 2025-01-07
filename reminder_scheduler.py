import sqlite3
import asyncio
import datetime

from model import DatabaseManager

db_manager = DatabaseManager()

async def reminder_schedule(bot):
    while True:
        try: 
            current_time_no_ms = datetime.datetime.now().replace(microsecond=0)

            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()

                cursor.execute('''
                    SELECT tasks.title, tasks.deadline, users.telegram_id, users.reminder_time
                    FROM tasks
                    JOIN users ON tasks.user_id = users.telegram_id
                    WHERE tasks.status = 0
                ''')
                tasks_to_remind = cursor.fetchall()

            for title, deadline, telegram_id, reminder_time in tasks_to_remind:
                deadline = datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
                time_left = deadline - current_time_no_ms

                if time_left == datetime.timedelta(hours=int(reminder_time)):
                    minutes_left = (deadline - current_time_no_ms).seconds // 60
                    await bot.send_message(
                        chat_id=telegram_id,
                        text=f'⏳ Напоминание! До задачи "{title}" осталось {minutes_left} минут.'
                        )
                
            await asyncio.sleep(1)
        
        except Exception:
            print('Произошла ошибка в планировщике напоминаний.')
            await asyncio.sleep(1)

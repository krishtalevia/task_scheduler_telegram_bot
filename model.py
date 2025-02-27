import sqlite3

def init_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id     INTEGER UNIQUE,
            is_authorized   BOOLEAN DEFAULT 0,
            reminder_time   INTEGER DEFAULT 1
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER,
            title           TEXT,
            description     TEXT,
            deadline        DATETIME,
            priority        TEXT,
            status          BOOLEAN,
            created_at      DATETIME,
            completed_at    DATETIME,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    ''')
    connection.commit()
    connection.close()

if __name__ == '__main__':
    init_db()

class DatabaseManager:
    def __init__(self, db_name='database.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def register_user(self, telegram_id):
        if self.get_user(telegram_id):
            raise ValueError('Пользователь уже существует!')
        self.cursor.execute('INSERT INTO users (telegram_id) VALUES (?)', (telegram_id,))
        self.connection.commit()
        return True
    
    def set_user_reminder_time(self, telegram_id, reminder_time):
        self.cursor.execute('UPDATE users SET reminder_time = ? WHERE telegram_id = ?', (reminder_time, telegram_id))
        self.connection.commit()
        return True
    
    def get_user(self, telegram_id):
        self.cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        return self.cursor.fetchone()
    
    def authorize_user(self, telegram_id):
        self.cursor.execute('SELECT is_authorized FROM users WHERE telegram_id = ?', (telegram_id,))
        result = self.cursor.fetchone()

        if result is None:
            raise ValueError('Пользователь не зарегистрирован.')
        
        if result[0] == 1:
            raise ValueError('Пользователь уже авторизован.')

        self.cursor.execute('UPDATE users SET is_authorized = 1 WHERE telegram_id = ?', (telegram_id,))
        self.connection.commit()
        return True

    def is_user_authorized(self, telegram_id):
        self.cursor.execute('SELECT is_authorized FROM users WHERE telegram_id = ?', (telegram_id,))
        result = self.cursor.fetchone()
        if result is None:
            raise ValueError('Пользователь не найден.')
        return result[0] == 1
    
    def logout_user(self, telegram_id):
        if self.is_user_authorized(telegram_id):
            self.cursor.execute('UPDATE users SET is_authorized = 0 WHERE telegram_id = ?', (telegram_id,))
            self.connection.commit()
            return True
        else:
            raise ValueError('Пользователь не авторизован.')
            return False
        
    def delete_user(self, telegram_id):
        self.cursor.execute('DELETE FROM users WHERE telegram_id = ?', (telegram_id,))
        self.connection.commit()
        return True
    
    def delete_all_users(self):
        self.cursor.execute('DELETE FROM users')
        self.connection.commit()
        return True

    def add_task(self, user_id, title, description, deadline, priority, created_at, completed_at=None, status=False):
        self.cursor.execute('''
            INSERT INTO tasks (user_id, title, description, deadline, priority, status, created_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, title, description, deadline, priority, int(status), created_at, completed_at))
        self.connection.commit()
    
    def get_tasks(self, user_id):
        self.cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()
    
    def get_task_by_id(self, user_id, task_id):
        self.cursor.execute('SELECT * FROM tasks WHERE user_id = ? AND id = ?', (user_id, task_id,))
        return self.cursor.fetchone()
    
    def get_tasks_by_keyword(self, user_id, keyword):
        keyword = f'%{keyword}%'
        self.cursor.execute('SELECT * FROM tasks WHERE user_id = ? AND (title LIKE ? OR description LIKE ?)', (user_id, keyword, keyword))
        return self.cursor.fetchall()
    
    def update_task(self, user_id, task_id, parameter_name, new_value):
        self.cursor.execute(f'UPDATE tasks SET {parameter_name} = ? WHERE user_id = ? AND id = ?', (new_value, user_id, task_id))
        self.connection.commit()
        return True

    def delete_task(self, user_id, task_id):
        self.cursor.execute(f'DELETE FROM tasks WHERE user_id = ? and id = ?', (user_id, task_id))
        self.connection.commit()
        return True
    
    def close(self):
        self.connection.close()
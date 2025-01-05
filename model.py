import sqlite3

def init_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id     INTEGER UNIQUE,
            is_authorized   BOOLEAN DEFAULT 0
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER,
            title           TEXT,
            description     TEXT,
            deadline        DATE,
            priority        TEXT,
            status          BOOLEAN,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    ''')
    connection.commit()
    connection.close()

if __name__ == '__main__':
    init_db()

class Task:
    def __init__(self, user_id, title, description, deadline, priority, status):
        self._user_id = user_id
        self._title = title
        self._description = description
        self._deadline = deadline
        self._priority = priority
        self._status = status

    @property
    def user_id(self):
        return self._user_id
    
    @property
    def title(self):
        return self._title
    
    @property
    def description(self):
        return self._description
    
    @property
    def deadline(self):
        return self._deadline
    
    @property
    def priority(self):
        return self._priority
    
    def __str__(self):
        task_info = f'Задача "{self._title}": {self._description} (приоритет: {self._priority}, выполнить до: {self._deadline}).'
        return task_info

class DatabaseManager:
    def __init__(self, db_name='database.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def register_user(self, telegram_id):
        try:
            self.cursor.execute('INSERT INTO users (telegram_id) VALUES (?)', (telegram_id,))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            raise ValueError('Пользователь уже существует.')
        
    def get_user(self, telegram_id):
        self.cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        return self.cursor.fetchone()
    
    def authorize_user(self, telegram_id):
        self.cursor.execute('SELECT is_authorized FROM users WHERE telegram_id = ?', (telegram_id,))
        result = self.cursor.fetchone()

        if result is None:
            raise ValueError('Пользователь не зарегистрирован.')
            return False
        
        if result[0] == 1:
            raise ValueError('Пользователь уже авторизован.')
            return False

        self.cursor.execute('UPDATE users SET is_authorized = 1 WHERE telegram_id = ?', (telegram_id,))
        self.connection.commit()
        return True

    def is_user_authorized(self, telegram_id):
        self.cursor.execute('SELECT is_authorized FROM users WHERE telegram_id = ?' (telegram_id,))
        result = self.cursor.fetchone()
        return True if result[0] == 1 else False
    
    def logout_user(self, telegram_id):
        if self.is_user_authorized(telegram_id):
            self.cursor.execute('UPDATE users SET is_authorized = 0 WHERE telegram_id = ?', (telegram_id,))
        else:
            raise Exception('Пользователь не авторизован.')

    def add_task(self, user_id, title, description, deadline, priority, status=False):
        self.cursor.execute('''
            INSERT INTO tasks (user_id, title, description, deadline, priority, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, title, description, deadline, priority, int(status)))
        self.connection.commit()
    
    def get_tasks(self, user_id):
        self.cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()
    
    def close(self):
        self.connection.close()
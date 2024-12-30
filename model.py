import sqlite3

def init_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id     INTEGER UNIQUE,
            username        TEXT
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
            completed       BOOLEAN,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    ''')
    connection.commit()
    connection.close()

if __name__ == '__main__':
    init_db()

class Task:
    def __init__(self, user_id, title, description, deadline, priority, completed):
        self._user_id = user_id
        self._title = title
        self._description = description
        self._deadline = deadline
        self._priority = priority
        self._completed = completed

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

    def register_user(self, telegram_id, username):
        try:
            self.cursor.execute('INSERT INTO users (telegram_id, username) VALUES (?, ?)', (telegram_id, username))
            self.connection.commit()
            return True
        except Exception:
            return False
        
    def get_user(self, telegram_id):
        self.cursor.execute('SELECT FROM users WHERE telegram_id = ?', (telegram_id))
        return self.cursor.fetchone()

    def add_task(self, user_id, title, description, deadline, priority, completed=False):
        if priority not in ['низкая', 'средняя', 'высокая']:
            raise ValueError('Приоритет может иметь одно из следующих значений: "низкая", "средняя" или "высокая".')
        self.cursor.execute('''
            INSERT INTO tasks (user_id, title, description, deadline, priority, completed)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, title, description, deadline, priority, int(completed)))
        self.connection.commit()
    
    def get_tasks(self, user_id):
        self.cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id))
        return self.cursor.fetchall()
    
    def close(self):
        self.connection.close()
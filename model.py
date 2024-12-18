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

class DatabaseManager:
    def __init__(self, db_name='database.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def register_user(self, telegram_id, username):
        try:
            self.cursor.execute('INSERT INTO users (telegram_id, username) VALUES (?, ?)', (telegram_id, username))
            self.connection.commit()
            return True
        except:
            return False

    def add_task(self, user_id, title, description, deadline, priority, completed=False):
        if priority not in ['низкая', 'средняя', 'высокая']:
            raise ValueError('Приоритет может иметь следующие значения: "низкая", "средняя" или "высокая".')
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
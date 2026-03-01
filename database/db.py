import aiosqlite

class DatabaseBot:
    def __init__(self):
        self.db = None


    async def connect_with_database(self):
        if self.db is None:
            self.db = await aiosqlite.connect("database.db")
            await self.db.execute('''CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            amount_correctly_solved_examples INTEGER NOT NULL,
            amount_solved_examples INTEGER NOT NULL)
            ''')
            await self.db.commit()


    async def add_user(self, user_id, username, first_name):
        await self.db.execute('''INSERT OR IGNORE INTO Users
            (id, username, first_name, amount_correctly_solved_examples, amount_solved_examples)
            VALUES (?, ?, ?, 0, 0)''',
            (user_id, username, first_name))
        await self.db.commit()


    async def update_stats(self, user_id, is_correct_ans):
        if is_correct_ans:
            await self.db.execute("UPDATE Users SET amount_correctly_solved_examples = amount_correctly_solved_examples + 1 WHERE id = ?", (user_id,))
        await self.db.execute("UPDATE Users SET amount_solved_examples = amount_solved_examples + 1 WHERE id = ?", (user_id,))
        await self.db.commit()


    async def get_user_stats(self):
        cursor = await self.db.execute('''SELECT first_name, amount_correctly_solved_examples
                        FROM Users 
                        ORDER BY amount_correctly_solved_examples DESC
                        LIMIT 5
                        ''')
        rows = await cursor.fetchall()
        return rows
    

    async def get_profile_statistics(self, user_id):
        cursor = await self.db.execute('''SELECT amount_solved_examples,
                            amount_correctly_solved_examples, first_name 
                            FROM Users WHERE id = ?''', (user_id,))
        rows = await cursor.fetchall()
        return rows

    
    async def close_connection(self):
        if self.db:
            await self.db.close()
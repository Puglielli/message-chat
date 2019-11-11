import sqlite3

conn = ""
cursor = ""


class ConnectionDatabase:
    def __init__(self, directory):
        global conn
        global cursor
        conn = sqlite3.connect(directory)
        cursor = conn.cursor()

    @staticmethod
    def formatter(line):
        line = str(line)
        line = line.replace("(", "")
        line = line.replace(")", "")
        line = line.replace("'", "")
        line = line.replace("[", "")
        line = line.replace("]", "")
        line = line.replace(",", "")
        return line

    @staticmethod
    def getName(table, id):
        query = f'SELECT name FROM {table} where id = {id}'
        return str(cursor.execute(query).fetchall())

    @staticmethod
    def getStep(table, id):
        query = f'SELECT step FROM {table} where id = {id}'
        return str(cursor.execute(query).fetchall())

    @staticmethod
    def getQuestions(table, id):
        query = f'SELECT questions FROM {table} where id = {id}'
        return str(cursor.execute(query).fetchall())

    @staticmethod
    def getAll(table):
        query = f'SELECT * FROM {table}'
        return str(cursor.execute(query).fetchall())

    @staticmethod
    def create(table):
        global cursor
        global conn

        cursor.execute(f'''
        CREATE TABLE  {table} (
                id INTEGER NOT NULL PRIMARY KEY,
                name TEXT,
                step TEXT NOT NULL,
                questions TEXT
                );
        ''')

    @staticmethod
    def insert(table, id, name, step, questions):
        global cursor
        global conn

        params = id, name, step, questions

        cursor.execute(f'''
        INSERT INTO {table} (id, name, step, questions)
            VALUES (?, ?, ?, ?)
        ''', params)
        conn.commit()

    @staticmethod
    def updateStep(table, id, step):

        cursor.execute(f'''
        UPDATE {table} SET 
        step = {step}
        WHERE id = {id};        
                ''')
        conn.commit()

    @staticmethod
    def updateName(table, id, name):

        cursor.execute(f'''
        UPDATE {table} SET 
        name = {name}
        WHERE id = {id};        
                ''')
        conn.commit()

    @staticmethod
    def updateQuestions(table, id, questions):

        cursor.execute(f'''
        UPDATE {table} SET 
        questions = {questions}
        WHERE id = {id};        
                ''')
        conn.commit()
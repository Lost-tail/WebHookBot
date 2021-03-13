import sqlite3
import os

class DataBase():
    def __init__(self):
        pass
        
    def create_connection(self):
        connection = sqlite3.connect(os.path.abspath(__file__).rsplit('\\',1)[0] + '\\db.sqlite')
        return connection
     
    def execute_query(self, query):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()
        
    def create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS status (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          status TEXT NOT NULL
        );
        """
        self.execute_query(query)
        query = """
        CREATE TABLE IF NOT EXISTS chat (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          chat TEXT NOT NULL
        );
        """
        self.execute_query(query)
        query = """
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT NOT NULL UNIQUE,
          chat_id INTEGER NOT NULL
        );
        """
        self.execute_query(query)
        
    def get_status(self):
        query = """SELECT status FROM status WHERE id=(SELECT max(id) FROM status);"""
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        connection.close()
        if result:
            return result[0]
        else:
            return result
        
    def add_status(self, status):
        query = """
        INSERT INTO
          status (status)
        VALUES
          ('{}');
        """.format(status)
        self.execute_query(query)
        
    def drop_status(self):
        query = """DELETE FROM status"""
        self.execute_query(query)
        
    def add_chat(self, message):
        query = """
        INSERT INTO
          chat (chat)
        VALUES
          ('{}');
        """.format(message)
        self.execute_query(query)
       
    def view_chat(self):
        query = """SELECT chat FROM chat;"""
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result
        
    def add_user(self, username, chat_id):
        query = """
        INSERT INTO
          users (username, chat_id)
        VALUES
          ('{}', {});
        """.format(username, chat_id)
        self.execute_query(query)
        
    def get_chat_id(self, username):
        query = """SELECT chat_id from users WHERE username='{}';""".format(username)
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        connection.close()
        if result:
            return result[0]
        else:
            return result

if __name__=='__main__':
    db = DataBase()
    db.create_tables()
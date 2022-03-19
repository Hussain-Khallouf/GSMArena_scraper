# from SqliteOrm import SqliteOrm
import sqlite3


class PhoneOrm:

    TABLE_NAME = "phones"

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def create_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
            phone_id INTEGER PRIMARY KEY,
            brand TEXT,
            name TEXT,
            price TEXT,
            announcement_year TEXT,
            display_size REAL,
            memory TEXT,
            OS TEXT
            )"""

        self.cursor.execute(query)
        self.connection.commit()

    def select(self, propertis="*"):
        query = f"SELECT {propertis} from {self.TABLE_NAME}"
        phones = self.cursor.execute(query)
        return phones.fetchall()

    def insert(self, phone_dic):
        query = f"""INSERT INTO {self.TABLE_NAME}(
            brand ,name ,price ,announcement_year , display_size , memory , OS )
            VALUES (?,?,?,?,?,?,?)"""
        values = [tuple(phone_dic.values())]
        self.cursor.executemany(query, values)
        self.connection.commit()

    def delete(self, id):
        query = f"DELETE FROM {self.TABLE_NAME} WHERE phone_id = {id};"
        self.cursor.execute(query)
        self.connection.commit()

    def update(self, id, phone):
        query = f""" UPDATE {self.TABLE_NAME}
            SET brand = ?,
            name = ?,
            price = ?,
            announcement_year = ?,
            display_size = ?, 
            memory=?,
            OS=?
            WHERE phone_id = ?"""
        self.cursor.execute(query, tuple([*phone.values(), id]))
        self.connection.commit()

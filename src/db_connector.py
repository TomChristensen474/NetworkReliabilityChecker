import sqlite3

from sqlite3 import Connection, Error


def create_connection(path) -> Connection | None:
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

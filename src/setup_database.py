import sqlite3

from sqlite3 import Connection, Error

def create_connection(path) -> Connection|None: 
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection("src/network_history.db")

if connection:
    cursor = connection.cursor()
    result = cursor.execute("CREATE TABLE IF NOT EXISTS network_history (id INTEGER PRIMARY KEY, datetime TEXT, average_ping REAL, packet_loss REAL, network_down BOOLEAN DEFAULT FALSE)")

    connection.close()
import sqlite3

from pythonping import ping
from sqlite3 import Connection, Error
from time import gmtime, strftime

def create_connection(path) -> Connection|None: 
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def ping_and_record():
    connection = create_connection("networy_history.db")

    # ping_result = ""
    if connection:
        cursor = connection.cursor()

        ping_result = ping('8.8.8.8', interval=1, verbose=False) # one ping every second
        time = strftime("%d %b %Y %H:%M:%S", gmtime())
        print(time)

         # option 3 requires success on MOST packets
        if ping_result.success(option=2): # type: ignore
            print("Average ping time (ms): " + str(ping_result.rtt_avg_ms))
            print("Packet loss: " + str(ping_result.packet_loss))
            data = (time, ping_result.rtt_avg_ms, ping_result.packet_loss, False)
        else:
            print("Network down")
            data = (time, None, ping_result.packet_loss, True)

        result = cursor.execute("INSERT INTO network_history VALUES(NULL, ?, ?, ?, ?)", data)
        connection.commit()
        
        connection.close()

ping_and_record()
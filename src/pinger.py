from pythonping import ping
from sqlite3 import Connection, Error
from time import gmtime, strftime
# from datetime import datetime

from src import db_connector

def ping_and_record():
    connection = db_connector.create_connection("network_history.db")

    # ping_result = ""
    if connection:
        cursor = connection.cursor()

        ping_result = ping('8.8.8.8', interval=1, verbose=False) # one ping every second
        datetime = strftime("%F %T", gmtime())
        # datetime = datetime.now()
        print(datetime)

         # option 3 requires success on MOST packets
        if ping_result.success(option=2): # type: ignore
            print("Average ping time (ms): " + str(ping_result.rtt_avg_ms))
            print("Packet loss: " + str(ping_result.packet_loss))
            data = (datetime, ping_result.rtt_avg_ms, ping_result.packet_loss, False)
        else:
            print("Network down")
            data = (datetime, None, ping_result.packet_loss, True)

        cursor.execute("INSERT INTO network_history VALUES(NULL, ?, ?, ?, ?)", data)
        connection.commit()
        
        connection.close()

ping_and_record()